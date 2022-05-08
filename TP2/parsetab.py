
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CONST ELSE ELSEIF ENDCONDITION ENDFOR ENDIF FOR IF VARIABLE WORDprog : comandoscomandos : comandos : comandos VARIABLEcomandos : comandos WORDcomandos : comandos CONSTcomandos : comandos IF WORD ENDCONDITION comandos alternative ENDIFcomandos : comandos FOR WORD ENDCONDITION comandos ENDFOR alternative : condition_singalternative : condition_reccondition_sing : ELSE comandoscondition_rec : condition_rec : condition_rec ELSEIF WORD  ENDCONDITION  comandos'
    
_lr_action_items = {'VARIABLE':([0,2,3,4,5,10,11,12,13,17,18,19,21,23,24,],[-2,3,-3,-4,-5,-2,-2,3,3,-2,-7,-6,3,-2,3,]),'WORD':([0,2,3,4,5,6,7,10,11,12,13,17,18,19,20,21,23,24,],[-2,4,-3,-4,-5,8,9,-2,-2,4,4,-2,-7,-6,22,4,-2,4,]),'CONST':([0,2,3,4,5,10,11,12,13,17,18,19,21,23,24,],[-2,5,-3,-4,-5,-2,-2,5,5,-2,-7,-6,5,-2,5,]),'IF':([0,2,3,4,5,10,11,12,13,17,18,19,21,23,24,],[-2,6,-3,-4,-5,-2,-2,6,6,-2,-7,-6,6,-2,6,]),'FOR':([0,2,3,4,5,10,11,12,13,17,18,19,21,23,24,],[-2,7,-3,-4,-5,-2,-2,7,7,-2,-7,-6,7,-2,7,]),'$end':([0,1,2,3,4,5,18,19,],[-2,0,-1,-3,-4,-5,-7,-6,]),'ELSE':([3,4,5,10,12,18,19,],[-3,-4,-5,-2,17,-7,-6,]),'ENDIF':([3,4,5,10,12,14,15,16,17,18,19,21,23,24,],[-3,-4,-5,-2,-11,19,-8,-9,-2,-7,-6,-10,-2,-12,]),'ELSEIF':([3,4,5,10,12,16,18,19,23,24,],[-3,-4,-5,-2,-11,20,-7,-6,-2,-12,]),'ENDFOR':([3,4,5,11,13,18,19,],[-3,-4,-5,-2,18,-7,-6,]),'ENDCONDITION':([8,9,22,],[10,11,23,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'prog':([0,],[1,]),'comandos':([0,10,11,17,23,],[2,12,13,21,24,]),'alternative':([12,],[14,]),'condition_sing':([12,],[15,]),'condition_rec':([12,],[16,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> prog","S'",1,None,None,None),
  ('prog -> comandos','prog',1,'p_prog','main.py',107),
  ('comandos -> <empty>','comandos',0,'p_comandos_vazios','main.py',111),
  ('comandos -> comandos VARIABLE','comandos',2,'p_comandos_VARIABLE','main.py',115),
  ('comandos -> comandos WORD','comandos',2,'p_comandos_WORD','main.py',120),
  ('comandos -> comandos CONST','comandos',2,'p_comandos_CONST','main.py',133),
  ('comandos -> comandos IF WORD ENDCONDITION comandos alternative ENDIF','comandos',7,'p_comandos_if','main.py',145),
  ('comandos -> comandos FOR WORD ENDCONDITION comandos ENDFOR','comandos',6,'p_comandos_for','main.py',149),
  ('alternative -> condition_sing','alternative',1,'p_alternative_cond_sing','main.py',154),
  ('alternative -> condition_rec','alternative',1,'p_alternative_cond_rec','main.py',158),
  ('condition_sing -> ELSE comandos','condition_sing',2,'p_condition_sing','main.py',163),
  ('condition_rec -> <empty>','condition_rec',0,'p_condition_rec_vazio','main.py',167),
  ('condition_rec -> condition_rec ELSEIF WORD ENDCONDITION comandos','condition_rec',5,'p_condition_rec','main.py',171),
]
