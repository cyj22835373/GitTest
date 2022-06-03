function img = checkerGen(radius_size_pix, checker_size_pix)

n = ceil(radius_size_pix/checker_size_pix);
d = n*checker_size_pix-radius_size_pix;
img = checkerboard(checker_size_pix, n, n);
img = img(1+d:end-d, 1+d:end-d);
img = img>0.5;
img = img(:,end:-1:1);
img = (img-0.5).*0.25 + 0.5;
img = cat(3,img,img,img);

end

