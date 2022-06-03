function [...
    img_inf_x_mm,img_inf_y_mm,...
    img_min_x_mm,img_min_y_mm,...
    img_ext_x_mm,img_ext_y_mm,...
    img_min_px_mm,img_min_py_mm,...
    img_ext_px_mm,img_ext_py_mm ...
    ] = cmsekMark (...
    fl_mm, ...
    rear_x_mm, vcam_x_mm, vcam_y_mm, vcam_z_mm, ...
    vcam_h_deg, vcam_v_deg, ...
    vclass ...
    )

org_min_x0_mm =-vcam_y_mm;
org_min_y0_mm = vcam_z_mm;
org_ext_x0_mm =-vcam_y_mm;
org_ext_y0_mm = vcam_z_mm;

if vclass == 0 % Class I
    org_min_x1_mm =-vcam_y_mm-10000;
    org_min_x2_mm =-vcam_y_mm+10000;
    org_min_z1_mm = vcam_x_mm+60000;
    org_min_z2_mm = vcam_x_mm+100000;
    org_ext_x1_mm =-vcam_y_mm-10000;
    org_ext_x2_mm =-vcam_y_mm+10000;
else
    if vclass < 3 % Class II
        org_min_x1_mm = 1000-vcam_y_mm;
        org_min_x2_mm = 5000-vcam_y_mm;
        org_min_z1_mm = vcam_x_mm+4000;
        org_min_z2_mm = vcam_x_mm+30000;
        org_min_z3_mm = vcam_x_mm+60000;
    elseif vclass < 5 % Class III
        org_min_x1_mm = 1000-vcam_y_mm;
        org_min_x2_mm = 4000-vcam_y_mm;
        org_min_z1_mm = vcam_x_mm+4000;
        org_min_z2_mm = vcam_x_mm+20000;
        org_min_z3_mm = vcam_x_mm+60000;
    else % Class IV
        org_min_x1_mm = 4500-vcam_y_mm;
        org_min_x2_mm = 15000-vcam_y_mm;
        org_min_z1_mm = vcam_x_mm+1500;
        org_min_z2_mm = vcam_x_mm+10000;
        org_min_z3_mm = vcam_x_mm+25000;
    end
    org_ext_x1_mm = 0;
end
org_ext_z1_mm = vcam_x_mm+rear_x_mm;

org_vec = zeros(3,8);
org_vec(:,1) = [0 0 1000000]';
MRX = vrrotvec2mat([1 0 0 vcam_v_deg*pi/180]);
if vclass == 0
    org_vec(:,2) = [org_min_x1_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,3) = [org_min_x0_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,4) = [org_min_x2_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,5) = [org_min_x2_mm org_min_y0_mm org_min_z2_mm]';
    org_vec(:,6) = [org_min_x1_mm org_min_y0_mm org_min_z2_mm]';
    org_vec(:,7) = [org_ext_x1_mm org_ext_y0_mm org_ext_z1_mm]';
    org_vec(:,8) = [org_ext_x2_mm org_ext_y0_mm org_ext_z1_mm]';
    MRY = vrrotvec2mat([0 -1 0 vcam_h_deg*pi/180]);
elseif mod(vclass,2) == 1
    org_vec(:,2) = [org_min_x0_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,3) = [org_min_x1_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,4) = [org_min_x2_mm org_min_y0_mm org_min_z2_mm]';
    org_vec(:,5) = [org_min_x2_mm org_min_y0_mm org_min_z3_mm]';
    org_vec(:,6) = [org_min_x0_mm org_min_y0_mm org_min_z3_mm]';
    org_vec(:,7) = [org_ext_x0_mm org_ext_y0_mm org_ext_z1_mm]';
    org_vec(:,8) = [org_ext_x1_mm org_ext_y0_mm org_ext_z1_mm]';
    MRY = vrrotvec2mat([0 -1 0 vcam_h_deg*pi/180]);
else
    org_vec(:,2) = [-org_min_x0_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,3) = [-org_min_x1_mm org_min_y0_mm org_min_z1_mm]';
    org_vec(:,4) = [-org_min_x2_mm org_min_y0_mm org_min_z2_mm]';
    org_vec(:,5) = [-org_min_x2_mm org_min_y0_mm org_min_z3_mm]';
    org_vec(:,6) = [-org_min_x0_mm org_min_y0_mm org_min_z3_mm]';
    org_vec(:,7) = [-org_ext_x0_mm org_ext_y0_mm org_ext_z1_mm]';
    org_vec(:,8) = [-org_ext_x1_mm org_ext_y0_mm org_ext_z1_mm]';
    MRY = vrrotvec2mat([0 -1 0 -vcam_h_deg*pi/180]);
end

img_vec = MRY*org_vec;
img_vec = MRX*img_vec;

img_x_mm = img_vec(1,:).*fl_mm./img_vec(3,:);
img_y_mm = img_vec(2,:).*fl_mm./img_vec(3,:);

img_inf_x_mm = img_x_mm(1);
img_inf_y_mm = img_y_mm(1);
img_min_x_mm = img_x_mm(2:6)';
img_min_y_mm = img_y_mm(2:6)';
img_ext_x_mm = img_x_mm(7:8)';
img_ext_y_mm = img_y_mm(7:8)';

istep = size(img_min_x_mm,1);
jstep = 8;

img_min_px_mm = zeros(istep*jstep,1);
img_min_py_mm = zeros(istep*jstep,1);
for i = 0:istep-1
    i_next = mod(i+1,istep);
    for j = 0:jstep-1
        img_min_px_mm(i*jstep+j+1) = img_min_x_mm(i+1)+j*(img_min_x_mm(i_next+1)-img_min_x_mm(i+1))/jstep;
        img_min_py_mm(i*jstep+j+1) = img_min_y_mm(i+1)+j*(img_min_y_mm(i_next+1)-img_min_y_mm(i+1))/jstep;
    end
end
img_ext_px_mm = zeros(jstep+1,1);
img_ext_py_mm = zeros(jstep+1,1);
for j = 0:jstep
    img_ext_px_mm(j+1) = img_ext_x_mm(1)+j*(img_ext_x_mm(2)-img_ext_x_mm(1))/jstep;
    img_ext_py_mm(j+1) = img_ext_y_mm(1)+j*(img_ext_y_mm(2)-img_ext_y_mm(1))/jstep;
end


end

