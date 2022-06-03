function [imgname] = GetUESenseImg(CameraPos,CameraAngle,f,imgSize)
%UNTITLED5 用户设置相机相对于车辆中心点的偏移，旋转角度，相机焦距，得到一张该场景下渲染的图片
%   此处提供详细说明
global imagesize CameraOPCenter CameraPosi CameraAngs CameraF;
global imagesizeP CameraOPCenterP CameraPosiP CameraAngsP CameraF_P;
imagesize = imgSize;
imagesizeP = imgSize;
CameraF = f
CameraF_P = f
CameraOPCenter = [imgSize(2)/2,imgSize(1)/2];
CameraOPCenterP = CameraOPCenter;
%这里要说明的是iWaySense CMS Evaluation Kit中的原点是 x：前轮 y：门 z：地面 而UE4的原点是 车辆正中间，地面点，二者需要变换一下
centerToFront = 1.491;
centerToRear  = 1.529;
frontOverhang = 0.983;
rearOverhang  = 0.945;
vehicleWidth  = 2.009;
vehicleHeight = 1.370;
CameraPosi = [centerToFront-CameraPos(1)/1000,vehicleWidth/2 - CameraPos(2)/1000,CameraPos(3)/1000];
CameraPosi(1)=0.38;
CameraPosiP = CameraPosi;
CameraPosiP(2) = -CameraPosiP(2);

CameraAngs = [180,-CameraAngle(2)+180,-CameraAngle(1)];
CameraAngsP = [180,-CameraAngle(2)+180,CameraAngle(1)];

options=simset('SrcWorkspace','current');
sim('straightRoadVideoRecording',[],options);


DriverMat = load('DriverSide.mat');
imwrite(DriverMat.ans.Data(:,:,:,1),"DriverSide.png");

PassengerMat = load('PassengerSide.mat');
imwrite(PassengerMat.ans.Data(:,:,:,1),"PassengerSide.png");

end