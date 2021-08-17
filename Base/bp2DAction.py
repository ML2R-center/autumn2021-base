
from bp2DBase import *
from bp2DState import *




class Action:

    def __init__(self, pnt, rct):
        self.rct = rct  # rectangle to be placed
        self.pnt = pnt  # point for rectangle to be placed at


    def __repr__(self):
        return 'action: r%d at (%f,%f)' % (self.rct.n, self.pnt[0], self.pnt[1])


    
    def complies_with_box(self, state): # checks whether rct is in bounds
        test = self.rct.place_at(self.pnt)
        return state.box.contains_rectangle(test)

    def complies_with_box_content(self, state): # checks that no rcts in box overlap
        test = self.rct.place_at(self.pnt)
        for rct in state.rcts_clsd:
            if test.overlap(rct) > 0: return False
        return True

    def is_feasible(self, state):
        return self.complies_with_box(state) and \
               self.complies_with_box_content(state)

    def apply_to(self, state):
        rcts_clsd = list(state.rcts_clsd) # recall that list([...])
        rcts_open = list(state.rcts_open) # creates a copy of [...]
        pnts_open = list(state.pnts_open)
        box       = state.box

        rct = self.rct
        pnt = self.pnt

        rcts_open.remove(rct) # works, because we overlaoded == in Rectangle2D
        pnts_open.remove(pnt) # works, because we overlaoded == in Point2D


        rct_new = rct.place_at(pnt)
        
        pnts_open.extend(Action.new_placing_points(rct_new, state)) # TODO: needed? not sure if blog entry code runs if this line is included
        rcts_clsd.append(rct_new)
        
        return State(rcts_clsd, rcts_open, pnts_open, box)



    def rot_rct(self):
        # forward method for 2DRct.rotate90()
        self.rct.rotate90()

    
    @staticmethod
    def new_placing_points(rct, state):
        box       = state.box
        rcts_clsd = state.rcts_clsd

        pnt_br = rct.get_corner('br')
        pnt_tl = rct.get_corner('tl')

        pnts_new = []


        # test w.r.t. the 1st candidate point 
        if pnt_br.get_x() < box.get_w():
            # test if bottom face of box contains candidate point
            if box.get_face('b').interior_contains_point(pnt_br):
                pnts_new.append(pnt_br)
            else:
                touches_tr = False
                touches_tl = False
                # iterate over all previously packed rectangles 
                for r in rcts_clsd:
                    # test if top face of rectangle contains candidate
                    if r.get_face('t').interior_contains_point(pnt_br):
                        pnts_new.append(pnt_br)
                        break
                    
                    if r.get_corner('tr') == pnt_br:
                        touches_tr = True
                    if r.get_corner('tl') == pnt_br:
                        touches_tl = True
                if touches_tr and touches_tl:
                    pnts_new.append(pnt_br)

                    
        # test w.r.t. the 2nd candidate point 
        if pnt_tl.get_y() < box.get_h():
            # test if left face of box contains candidate point
            if box.get_face('l').interior_contains_point(pnt_tl):
                pnts_new.append(pnt_tl)
            else:
                touches_br = False
                touches_tr = False
                # iterate over all previously packed rectangles 
                for r in rcts_clsd:
                    # test if right face of rectangle contains candidate
                    if r.get_face('r').interior_contains_point(pnt_tl):
                        pnts_new.append(pnt_tl)
                        break
                    
                    if r.get_corner('br') == pnt_tl:
                        touches_tr = True
                    if r.get_corner('tr') == pnt_tl:
                        touches_tl = True ## TODO: bug? maybe this broke 2DRct.contains_point()?
                if touches_br and touches_tr:
                    pnts_new.append(pnt_tl)
            
        return pnts_new 
        

    
if __name__ == '__main__':
    pass


