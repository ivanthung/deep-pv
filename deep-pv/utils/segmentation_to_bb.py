def segmentation_to_bb():
    segmentation = [4306.366298, 119.667347, 4307.074, 114.6348, 4278.526, 115.4772, 4276.3732, 126.7092, 4295.739662, 126.646727, 4305.730051, 126.825127, 4306.366298, 119.667347]
    coords = [[segmentation[coord], segmentation[coord+1]] for coord in range(0, len(segmentation)-1, 2)]
    x = [ x_coord[0] for x_coord in coords]
    y = [ y_coord[1] for y_coord in coords]

    xmax = max(x)
    xmin =
    ymax = max(y)
    ymin = min(y)
    return (min(x), xmax, ymin, ymax)
