# v2e
[v2e github](https://github.com/SensorsINI/v2e)  
```
git clone https://github.com/SensorsINI/v2e.git
cd v2e
```
v2e 폴더에 들어갑니다.  
```
conda create -n v2e-env python=3.8  # create a new environment
source activate v2e-env  # activate the environment
python setup.py develop
```
위 과정으로 v2e를 위한 환경 설정을 마칩니다.
[저자 제공 샘플 데이터 다운](https://drive.google.com/file/d/1dNUXJGlpEM51UVYH4-ZInN9pf0bHGgT_/view?usp=sharing)해당 데이터를 input 폴더를 만들고 안에 넣어줍니다.
```
python v2e.py -i input/tennis.mov --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.005 --output_folder=output/tennis --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 tennis.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 
```
위 명령어를 입력해 v2e를 실행합니다.  
slomo를 사용하지 않으려면
```
python v2e.py -i input/tennis.mov --overwrite --timestamp_resolution=.003 --auto_timestamp_resolution=False --dvs_exposure duration 0.005 --output_folder=output/tennis --overwrite --pos_thres=.15 --neg_thres=.15 --sigma_thres=0.03 --dvs_aedat2 tennis.aedat --output_width=346 --output_height=260 --stop_time=3 --cutoff_hz=15 --disable_slomo
```
위 명령어를 입력합니다.

### 다른 중요한 파라미터들

노이즈가 적은 output event signal을 생성
```
--dvs_params clean
```
프레임 간격을 조절하는 파라미터.  
블렌더에서 480FPS로 3초간 녹화시 1440프레임이 생성되기 때문에 아래와 같은 타임으로 설정해야함
```
--dvs_exposure duration 0.00208333
```
