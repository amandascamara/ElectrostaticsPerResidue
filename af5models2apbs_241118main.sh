#!/bin/bash

 folder="/filer-dg/agruppen/DG/camara/AlphaFold_models/FZP/$f/"
 cd $folder
 for ((i=0; i<=4; i=i+1))
 do
  pdb2pqr --ff=AMBER ranked_$i\.pdb mol_$i\.pqr --apbs-input mol_$i.in
  sed -i -e "s/write pot dx mol_$i.pqr/ion charge +1 conc 0.15 radius 2.0\n    ion charge -1 conc 0.15 radius 1.8\n    write atompot flat mol_$i.pqr/g" mol_$i.in
  apbs mol_$i\.in > mol_$i\.out
 done
done

 python apbsoutplot_epot.py $outfolder

###### versions
# APBS 3.4.1
# pdb2pqr 3.6.2
