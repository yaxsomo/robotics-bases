import math
import constants

def computeDK(theta1, theta2, theta3):
    alpha = theta2 + theta3
    p2_z = constants.constL2  * math.sin(theta2)
    L2_proj = math.cos(theta2) * constants.constL2
    L3_proj = constants.constL3 * math.cos(alpha)
    L_proj = constants.constL1 + L2_proj + L3_proj
    p3_x = L_proj * math.cos(theta1)
    p3_y = L_proj * math.sin(theta1)
    p3_z = p2_z + (constants.constL3 * math.sin(alpha))
    result = [p3_x, p3_y, -p3_z]
    return result
    
def computeIK():
    return

    
