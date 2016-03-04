bw=37;
bl=20;
bh=2;
sw=2;
sl=bl/2;
sh=17;
dw1=10+2;
dw2=25;
dl=bl/2;
dh=2;

difference(){
    
union(){
    //Upper board
    translate([0,0,15]) cube([bw+4,bl,bh]);
    translate([0,(bl/2),0]) cube([sw,sl,sh]);
    translate([bw+2,(bl/2),0]) cube([sw,sl,sh]);
    translate([-dw1,bl/2,0]) cube([dw1,dl,dh]);
    translate([bw+2,bl/2,0]) cube([dw2,dl,dh]);
    
}

translate([-(dw1/2)-1,(bl/2)+(dl/2),-5]) cylinder(r=2.25,h=30,$fn=50);
translate([-(dw1/2)-1+66,(bl/2)+(dl/2),-5]) cylinder(r=2.25,h=30,$fn=50);
translate([(bw/2)-2,(bl/2)-5,0]) cube([10,2,30]);

}

