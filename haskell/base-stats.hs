#!/usr/bin/ghci

data Character = C { strength,
                     perception,
                     endurance,
                     charisma,
                     intelligence,
                     agility,
                     luck,
                     magic,
                     ranging,
                     regen :: Int
                   }

data Damage :: Int

attack :: Character -> Damage
attack (C { strength }) = 

