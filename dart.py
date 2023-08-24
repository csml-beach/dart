
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge


def plot_dartboard(x,y):

    colors = ['black','red']*10
    patches= []


    # Define the radii for the bands
    radii = [ 0.1, 0.2, 0.35, 0.55, 0.80, 1.0]

    # Plot the bands of colors
    for i in range(len(radii)-1):
        color = colors[i]

        wedge = Wedge((0, 0), radii[i+1], 0, 360, width=radii[i+1]-radii[i], facecolor=color)
        plt.gca().add_patch(wedge)
        
    plt.scatter(x,y, marker = '+', s=100, c='w')
    plt.axis('scaled')
    plt.gca().set_facecolor("grey")


def simulate_3d_dart_throw(angle_x, angle_y,
                           initial_position = [0,0,0],
                           initial_velocity = 15.0,
                           time_step = 0.01,
                           plot = False):
    '''
    This function solves the trajectory of the dart. 
    Use the required inputs: angle_x and angle_y
    and pass scalar values (not arrays) to the function.   This function returns the position of the dart 
    where it (approximately) hits the board. 
    
    You can set the plot 
    flag to True to visualize where a random throw 
    with these input angles would land. 

    '''
    # Convert the angles from degrees to radians

    sigma =  1

    angle_x +=  sigma*np.random.randn(1) 
    angle_y +=  sigma*np.random.randn(1) 

    angle_x = math.radians(angle_x )
    angle_y = math.radians(angle_y )

    # Initialize lists to store the position of the dart at each time step
    x_positions = [initial_position[0]]
    y_positions = [initial_position[1] + 0.5]
    z_positions = [initial_position[2]]

    # Calculate the initial velocity components
    initial_velocity_x = initial_velocity * math.cos(angle_x) * math.cos(angle_y)
    initial_velocity_y = initial_velocity * math.sin(angle_x) * math.cos(angle_y)
    initial_velocity_z = initial_velocity * math.sin(angle_y)

    # Simulate the dart throw until it hits the ground (z position becomes negative)
    while x_positions[-1]  <= 5:
        # Calculate the new position and velocity
        new_x = x_positions[-1] + initial_velocity_x * time_step
        new_y = y_positions[-1] + initial_velocity_y * time_step
        new_z = z_positions[-1] + initial_velocity_z * time_step - 0.5 * 9.8 * time_step ** 2
        new_velocity_x = initial_velocity_x
        new_velocity_y = initial_velocity_y
        new_velocity_z = initial_velocity_z - 9.8 * time_step

        # Update the position and velocity
        x_positions.append(new_x)
        y_positions.append(new_y)
        z_positions.append(new_z)
        initial_velocity_x = new_velocity_x
        initial_velocity_y = new_velocity_y
        initial_velocity_z = new_velocity_z

    if plot: plot_dartboard(y_positions[-1],z_positions[-1])

    return np.reshape(np.array([y_positions[-1], z_positions[-1]]), [-1,2])



def plot_hits_on_dartboard(angle_x,angle_y):

    hits = []
    for i in range(10):
        # Simulate the 3D dart throw
        hits.append(simulate_3d_dart_throw(angle_x, angle_y, plot=0))

    hits = np.array(hits).squeeze()
    print('Average distance to bulls eye = {:f} '.format(np.mean(np.square((hits)))))
    plot_dartboard(hits[:,0], hits[:,1])
    plt.savefig('darts.png')


def find_optimal_throw_angles():
    '''
    Implement your solution here.
    You can use the function simulate_3d_dart_throw
    to test a few  trial angles to get 
    some data to work with. 

    To goal is to find optimal angles
    in x and y directions
    such that the darts land close to  the origin (0,0).
    
    Once you have your solution, commit it to a new branch
    and create a pull request on GitHub.

    '''
    # Testing the angles from -15 to 15, this can be changed
    x_range = np.linspace(-15, 15, 15)
    y_range = np.linspace(-15, 15, 15)

    optimal_distance = float('inf')
    optimal_theta_x = 0
    optimal_theta_y = 0

    # loop over all the combinations of x & y and hit the board
    for x in x_range:
        for y in y_range:
            hits = []
            for hit in range(10):
                hits.append(simulate_3d_dart_throw(x, y, plot=False))

            hits = np.squeeze(np.array(hits))
            squared_distances = np.square(hits)
            avg_squared_distance = np.mean(squared_distances)

            # find the best x & y angles from optimal distance
            if avg_squared_distance < optimal_distance:
                optimal_distance = avg_squared_distance
                optimal_theta_x = x
                optimal_theta_y = y

    return optimal_theta_x, optimal_theta_y


if __name__ == "__main__":

    theta_x, theta_y = find_optimal_throw_angles()

    # Dont change the following lines:
    theta_x, theta_y = find_optimal_throw_angles()
    plot_hits_on_dartboard(angle_x = theta_x, angle_y=theta_y)
