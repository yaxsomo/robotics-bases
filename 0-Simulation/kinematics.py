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


def computeIK(p3_x, p3_y, p3_z):
    
    p3_z = -p3_z
    d13 = math.sqrt(p3_x**2 + p3_y**2) - constants.constL1
    a = math.atan2(p3_z,d13)
    d = math.sqrt(d13**2 + p3_z**2)

    alpha_feed = (constants.constL3**2 + constants.constL2**2 - d**2) / (2* constants.constL2 * constants.constL3 )

    if(alpha_feed > 1.0):
        alpha_feed = 1.0
    elif(alpha_feed < -1.0):
        alpha_feed=-1.0

    alpha = math.acos(alpha_feed)
    
    beta_feed = (constants.constL2**2 + d**2 - constants.constL3**2)/ (2* d * constants.constL2)

    if(beta_feed > 1.0):
        beta_feed = 1.0
    elif(beta_feed < -1.0):
        beta_feed=-1.0
    beta = math.acos(beta_feed)



    theta1 = math.atan2(p3_y,p3_x)

    theta2 = a + beta
    theta3 = math.pi + alpha

    return [theta1, theta2, theta3]
