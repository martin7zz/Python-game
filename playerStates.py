from enum import Enum

class MovementState(Enum):
    IDLE = 0
    RUN = 1
    JUMP = 2
    FALL = 3
    DASH = 4
    
class CombatState(Enum):
    NEUTRAL = 0
    ATTACK = 1
    HURT = 2
    KNOCKBACK = 3
