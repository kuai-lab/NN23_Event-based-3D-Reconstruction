import numpy as np

import torch
import torch.nn as nn

class PatchEmbed(nn.Module):
    
    def __init__(self, img_size=256, patch_size=32, window_size=4, in_chans=2, embed_dim=2048):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2
        self.window_size = window_size
        self.embed_dim = embed_dim
        
        self.proj = nn.Conv2d(
            in_chans,
            embed_dim,
            kernel_size=patch_size,
            stride=patch_size,
        )
        
    def forward(self, x):   # (batch_size, n_windows, in_chans, img_size, img_size) > (32, 4, 2, 256, 256)
        x = x.flatten(0,1)  # (batch_size * n_windows, in_chans, img_size, img_size) > (32*4, 2, 256, 256)
        x = self.proj(x)    # (batch_size * n_windows, embed_dim, n_patches ** 0.5, n_patches ** 0.5) > (32*4, 2048, 8, 8)
        x = x.flatten(2)    # (batch_size * n_windows, embed_dim, n_patches) > (32*4, 2048, 64)
        x = x.reshape(-1, self.window_size, self.embed_dim, self.n_patches) # > (32, 4, 2048, 64)
        x = x.transpose(2,3).flatten(1,2) # (batch_size, n_windows * n_patches, embed_dim) > (32, 4 * 64, 2048) 

        return x
    
    
class Attention(nn.Module):
    
    def __init__(self, dim, n_heads=16, qkv_bias = True, attn_p=0., proj_p=0.):
        super().__init__()
        self.n_heads = n_heads
        self.dim = dim
        self.head_dim = dim // n_heads
        self.scale = self.head_dim ** -0.5
        
        self.qkv = nn.Linear(dim, dim*3, bias = qkv_bias)
        self.attn_drop = nn.Dropout(attn_p)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_p)
        
    def forward(self, x, value=None, key=None):    # (n_samples, n_patches , dim) > (4, 64, 2048)
        n_samples, n_tokens, dim = x.shape
        
        if dim != self.dim:
            raise ValueError
        
        qkv = self.qkv(x)    # (n_samples, n_patches , 3 * dim) > (4, 64, 3*2048)
        qkv = qkv.reshape(   
            n_samples, n_tokens, 3, self.n_heads, self.head_dim
        )                    # (n_samples, n_patches , 3 , n_heads, head_dim) > (4, 64, 3, 16, 128)
        qkv = qkv.permute(2,0,3,1,4) # (3, n_samples, n_heads, n_patches, head_dim) > (3, 4, 16, 64, 128)
        
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        if(value!=None):
            v = value.reshape(   
                n_samples, n_tokens, 1, self.n_heads, self.head_dim
            ).permute(2,0,3,1,4)[0]
            
        if(key!=None):
            k = key.reshape(   
                n_samples, n_tokens, 1, self.n_heads, self.head_dim
            ).permute(2,0,3,1,4)[0]
            
        k_t = k.transpose(-2, -1) # (n_samples, n_heads, head_dim, n_patches) > (4, 16, 128, 64)
        
        dp = (
            q @ k_t
        ) * self.scale      # (n_samples, n_heads, n_patches, n_patches) > (4, 16, 64, 64)
        
        attn = dp.softmax(dim = -1)      # (n_samples, n_heads, n_patches, n_patches) > (4, 16, 64, 64)
        attn = self.attn_drop(attn)
        
        weighted_avg = attn @ v # (n_samples, n_heads, n_patches, head_dim) > (4, 16, 64, 128)
        weighted_avg = weighted_avg.transpose(1,2) # (n_samples, n_patches, n_heads, head_dim) > (4, 64, 16, 128)
        weighted_avg = weighted_avg.flatten(2) # (n_samples, n_patches, dim) > (4, 64, 2048)
        
        x = self.proj(weighted_avg) # (n_samples, n_patches, dim) > (4, 64, 2048)
        x = self.proj_drop(x) # (n_samples, n_patches, dim) > (4, 64, 2048)
        
        return x
    

    
class MLP(nn.Module):
    
    def __init__(self, in_features, hidden_features, out_features, p=0.):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(p)
        
    def forward(self, x): # (n_samples, n_patches, in_features) > (4, 64, 2048)
        x = self.fc1(x)    # (n_samples, n_patches, hidden_features) > (4, 64, 512)
        x = self.drop(self.act(x))
        x = self.fc2(x)    # (n_samples, n_patches, out_features) > (4, 64, 2048)
        x = self.drop(x)
        return x
    
    
class Block(nn.Module):
    
    def __init__(self, dim, n_heads, mlp_ratio=4.0, qkv_bias = True, p=0., attn_p = 0.):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim, eps=1e-6)
        self.attn = Attention(
            dim,
            n_heads=n_heads,
            qkv_bias=qkv_bias,
            attn_p=attn_p,
            proj_p=p
        )
        self.norm2= nn.LayerNorm(dim, eps=1e-6)
        hidden_features = int(dim * mlp_ratio)
        self.mlp = MLP(
            in_features=dim,
            hidden_features=hidden_features,
            out_features=dim,
        )
        
    def forward(self, x):
        x = x + self.attn(self.norm1(x))
        x = x + self.mlp(self.norm2(x))    
        
        return x

    
class DecoderBlock(nn.Module):
    
    def __init__(self, dim, n_heads, mlp_ratio=4.0, qkv_bias = True, p=0., attn_p = 0.):
        super().__init__()
        self.norm = nn.LayerNorm(dim, eps=1e-6)
        self.attn = Attention(
            dim,
            n_heads=n_heads,
            qkv_bias=qkv_bias,
            attn_p=attn_p,
            proj_p=p
        )
        self.block = Block(
                    dim = dim,
                    n_heads = n_heads,
                    mlp_ratio = mlp_ratio,
                    qkv_bias = qkv_bias,
                    p = p,
                    attn_p = attn_p
        )
        self.dropout = nn.Dropout(p)
        
        
    def forward(self, x, value, key):
        x = x + self.attn(self.norm(x), value, key)
        x = self.dropout(self.block(x))
        
        return x


    
class Decoder(nn.Module):
    
    def __init__(self, img_size=256, patch_size=32, window_size=4, in_chans=2, embed_dim=2048):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.n_patches = (img_size // patch_size) ** 2
        self.embed_dim = embed_dim
        self.window_size = window_size
        self.in_chans = in_chans
        
        self.proj = nn.ConvTranspose2d(
            embed_dim*window_size,
            in_chans,
            kernel_size=patch_size,
            stride=patch_size,
        )
        
    def forward(self, x):
        #print(x.shape) # (32, 4 * 64, 2048)
        x = x.reshape(-1, self.window_size, self.n_patches, self.embed_dim) # > (32, 4, 64, 2048)
        x = x.transpose(2,3) # > (32, 4, 2048, 64)
        x = x.flatten(1,2) # > (32, 4*2048, 64)
        x = x.view(-1, self.window_size * self.embed_dim, int(self.n_patches**0.5), int(self.n_patches**0.5)) # > (32, 4*2048, 8, 8)
        x = self.proj(x) # (n_samples, n_patches, embed_dim) > (32, 2, 256, 256)
        x = x.reshape(-1, 1, self.in_chans, self.img_size, self.img_size) # > (32, 4, 2, 256, 256)

        return x
    
    
class Transformer(nn.Module):
    def __init__(self,
                 img_size=256,
                 patch_size=32,
                 in_chans=2,
                 window_size=4,
                 embed_dim=512,
                 depth=6,
                 n_heads=16,
                 mlp_ratio=4.0,
                 qkv_bias=True,
                 p=0.,
                 attn_p=0.,
                ):
        super().__init__()
        
        self.patch_embed = PatchEmbed(
            img_size = img_size,
            patch_size = patch_size,
            in_chans = in_chans,
            window_size = window_size,
            embed_dim = embed_dim,
        )
        
        self.pos_embed = nn.Parameter(
            torch.zeros(1, self.patch_embed.n_patches * window_size, embed_dim)
        )
        self.pos_drop = nn.Dropout(p=p)
        
        self.blocks = nn.ModuleList(
            [
                Block(
                    dim = embed_dim,
                    n_heads = n_heads,
                    mlp_ratio = mlp_ratio,
                    qkv_bias = qkv_bias,
                    p = p,
                    attn_p = attn_p,
                )
                for _ in range(depth)
            ]
        )
        
        self.decoderblocks = nn.ModuleList(
            [
                DecoderBlock(
                    dim = embed_dim,
                    n_heads = n_heads,
                    mlp_ratio = mlp_ratio,
                    qkv_bias = qkv_bias,
                    p = p,
                    attn_p = attn_p,
                )
                for _ in range(depth)
            ]
        )
        
        self.norm = nn.LayerNorm(embed_dim, eps=1e-6)
        self.decoder = Decoder(
            img_size = img_size,
            patch_size = patch_size,
            in_chans = in_chans,
            window_size = window_size,
            embed_dim = embed_dim,
        )
        self.query_pos = nn.Parameter(
            torch.zeros(1, self.patch_embed.n_patches * window_size, embed_dim)
        )
    def forward(self, x):
        n_samples = x.shape[0]
        x = self.patch_embed(x)
        x = x + self.pos_embed
        x = self.pos_drop(x)
        
        for block in self.blocks:
            x = block(x)
        for decoderblock in self.decoderblocks:
            x = decoderblock(self.query_pos.repeat(x.shape[0],1,1), x, x)
            
        x = self.norm(x)
        
        x = self.decoder(x)
        return x
