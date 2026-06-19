from enum import Enum

class AIState(Enum):
    IDLE = 0
    PATROL = 1
    CHASE = 2
    ATTACK = 3
    
    
class MovementState(Enum):
    IDLE = 0
    RUN = 1
    JUMP = 2
    FALL = 3
    
class CombatState(Enum):
    NEUTRAL = 0
    ATTACK = 1
    HURT = 2
    STUNNED = 3
    KNOCKBACK = 4
    DEAD = 5

