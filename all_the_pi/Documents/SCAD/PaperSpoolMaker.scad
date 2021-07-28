/* Paper spool for PiPrinter project
 * 
 * Assume paper is 2.25" wide x 150ft long x 0.1mm thick
 * Need 458.34 meters of paper: 1,504.823 ft of paper
 * Thus need 11 rolls of paper.
 *
 * BUT must fit all 11 rolls of paper on the spool
 * thus need to fit 502.92 meters of paper on the spool
 * the outer diameter (outer_spool_radius) is thus 126.7mm (See piday.m)
 * assuming a core radius outer of 15/2 mm. 
 * 
 * ----- NOMINAL VALUES -----
 * outer_spool_radius = 126.7;	// from geometric center, mm
 * outer_core_radius = 15/2;	// mm
 * inner_core_radius = 5;	// bore hole, mm
 * end_cap_thickness = 3;	// mm
 * core_length = 60.375;	// mm
 * wall_thickness = outer_core_radius - inner_core_radius;	// mm
 * --------------------------
 * 
 * Need a way to hold the spool during printing. If the spool 
 * 	gets too large in diameter it will require a holding apparatus
 * 	that is very tall. It might be easier to design an apparatus
 * 	that instead clamps to the edge of a table/desk and holds the 
 * 	spool off the edge of the desk. The motor would be attached to 
 * 	the holding apparatus at the spool axis-pin/axle. 
 */

use <sleeve_bearing_mmc_6338k564.scad>
use <rotary_rod_1327k103.scad>

$fs = 0.5;	// minimum size of a fragment
$fa = 2;	// minimum angle of a fragment
oal = 2*3+60.375;	// mm


// axis
//color("green") rotary_rod_1327k105();	// 3/16" x 5" long rod

// bearings
//translate([0,0,-oal/2]) color("red") bearing_6338k564();
//translate([0,0,oal/2]){
//	rotate([0,180,0]){
//		color("red") bearing_6338k564();
//	}
//}


// spool with bearing cutouts
translate([0,0,-oal/2]){
	difference(){
		spool();
		bearing_6338k564();
		translate([0,0,oal]){
			rotate([0,180,0]){
				bearing_6338k564();
			};
		};
	};
};


/* ----- MODULE DEFINITIONS ----- */

module spool(osr=126.7, ocr=15/2, icr=5, ect=3, cl=60.375){
	/* Make the entire spool
	 *
	 * osr = outer spool radius, mm
	 * ocr = outer core radius, mm
	 * icr = inner core radius, mm
	 * ect = end cap thickness, mm
	 * cl = core length, mm
	 * wt = wall thickness, mm
	 */
	wt = ocr - icr;	// mm
	
	difference(){
		spool_no_hole(ect=ect, osr=osr, ocr=icr, cl=cl, wt=wt);
		translate([0,0,-0.25]){
			cylinder(r=icr, h=cl + 2*ect + 0.5);
		};
	}
}
module spool_no_hole(ect, osr, ocr, cl, wt){
	/* Make the entire spool with no bore hole
	 *
	 * ect = end cap thickness, mm
	 * osr = outer spool radius, mm
	 * ocr = outer core radius, mm
	 * cl = core length, mm
	 * wt = wall thickness, mm
	 */
	end_caps(ect=ect, osr=osr);
	translate([0,0,ect]){
		core(ir=ocr, wt=wt, cl=cl);
	};
	translate([0,0,ect + cl]){
		end_caps(ect=ect, osr=osr);
	};
};

module core(ir, wt, cl){
	/* Make the outer core 
	 *
	 * ir = inner_radius, mm
	 * wt = thickness of the core wall, mm
	 * cl = length of the core, mm
	 */
	cylinder(r=ir+wt, h=cl);
}

module end_caps(ect, osr){
	/* Make the end cap
	 *
	 * ect = end cap thickness, mm
	 * osr = outer spool radius, mm
	 */
	cylinder(r=osr, h=ect);
}