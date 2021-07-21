import numpy as np
import math


def npz_data(npz):
    query = np.load(npz)
    return query['intrinsic_mat'], query['extrinsic_mat'], query['depth_map']


def generate_pointcloud(depth, intrinsic, extrinsic, scalingFactor):
    focalLength = intrinsic[0][0]
    centerX = intrinsic[1][2]
    centerY = intrinsic[0][2]
    
    points = []    
    for v in range(depth.shape[1]):
        for u in range(depth.shape[0]):
            Z = depth[u,v] / scalingFactor
            if Z<=0: continue
            X = (u - centerX) * Z / focalLength
            Y = (v - centerY) * Z / focalLength
            points.append([X, Y, Z])
    ones = np.ones(len(points), dtype=np.float32)
    
    result = np.vstack((np.array(points).T, ones)).T 
    
    return np.dot(extrinsic, result.T).T


def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def rotationMatrixToEulerAngles(R) :

    # assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return x, y, z