function [imgname] = GetUESenseImg(CameraPos,CameraAngle,f,imgSize,rearW2ORP,ORP2CDx)
%UNTITLED5 用户设置相机相对于车辆中心点的偏移，旋转角度，相机焦距，得到一张该场景下渲染的图片
%   此处提供详细说明
global imagesize CameraOPCenter CameraPosi CameraAngs CameraF;
global imagesizeP CameraOPCenterP CameraPosiP CameraAngsP CameraF_P MyWheelBase;

imagesize = imgSize;
imagesizeP = imgSize;
CameraF = f
CameraF_P = f
CameraOPCenter = [imgSize(2)/2,imgSize(1)/2];
CameraOPCenterP = CameraOPCenter;
%这里要说明的是iWaySense CMS Evaluation Kit中的原点是 x：前轮 y：门 z：地面 而UE4的原点是 车辆正中间，地面点，二者需要变换一下
% SUV
% centerToFront = 1.422;
% centerToRear  = 1.474;
% frontOverhang = 0.991;
% rearOverhang  = 0.939;
% vehicleWidth  = 1.935;
% vehicleHeight = 1.774;

%pick
centerToFront = 1.842;
centerToRear  = 1.854;
frontOverhang = 1.124;
rearOverhang  = 1.321;
vehicleWidth  = 2.073;
vehicleHeight = 1.990;

ORP2Rear = centerToRear-ORP2CDx/1000;
WDx = rearW2ORP/1000 - ORP2Rear;
CameraPosi = [CameraPos(1)/1000-ORP2CDx/1000+WDx,vehicleWidth/2 - CameraPos(2)/1000+0.05,CameraPos(3)/1000];



%CameraPosi(1)= 0.38;
CameraPosiP = CameraPosi;
CameraPosiP(2) = -CameraPosiP(2);

CameraAngs = [180,-CameraAngle(2)+180,-CameraAngle(1)];
CameraAngsP = [180,-CameraAngle(2)+180,CameraAngle(1)];
%WheelBase = rearW2ORP/1000 + CameraPos(1)/1000;
MyWheelBase = 3.0;
options=simset('SrcWorkspace','current');
sim('straightRoadVideoRecording',[],options);


DriverMat = load('DriverSide.mat');
imwrite(DriverMat.ans.Data(:,:,:,2),"DriverSide.png");

PassengerMat = load('PassengerSide.mat');
imwrite(PassengerMat.ans.Data(:,:,:,2),"PassengerSide.png");

end