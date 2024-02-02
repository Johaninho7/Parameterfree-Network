import numpy as np


"""""
def dominate(labelList):
	# List to save the iterators of dominated labels
	dominatedLabels = []

	# Compare the last added label to the existing labels
	lastLabel = len(labelList)-1
	lastInPathLastLabel = len(labelList[lastLabel].detailedPath)-1
	for i in range(len(labelList)-1):
		lastInPath = len(labelList[i].detailedPath)-1
		# Can only dominate a label if the two compared labels have visited the same node as their last visit
		if (labelList[lastLabel].detailedPath[lastInPathLastLabel] == labelList[i].detailedPath[lastInPath]):
			# If both labels are equal we dominate the latest added label
			if (labelList[lastLabel].time == labelList[i].time and labelList[lastLabel].drive_R == labelList[i].drive_R and labelList[lastLabel].drive_B == labelList[i].drive_B and labelList[lastLabel].elapsed_R == labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) == np.asarray(labelList[i].elem))):
				labelList[lastLabel].done = True
				dominatedLabels.append(lastLabel)
				# If latest added label is dominated we can abort
				break
		elif (labelList[lastLabel].time <= labelList[i].time and labelList[lastLabel].drive_R <= labelList[i].drive_R and labelList[lastLabel].drive_B <= labelList[i].drive_B and labelList[lastLabel].elapsed_R <= labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) <= np.asarray(labelList[i].elem))):
			# Only register dominance if the label has not already been dominated or completed processing
			if (labelList[i].done == False):
				labelList[i].done = True
				dominatedLabels.append(i)
		elif (labelList[lastLabel].time >= labelList[i].time and labelList[lastLabel].drive_R >= labelList[i].drive_R and labelList[lastLabel].drive_B >= labelList[i].drive_B and labelList[lastLabel].elapsed_R >= labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) >= np.asarray(labelList[i].elem))):
				labelList[lastLabel].done = True
				dominatedLabels.append(lastLabel)
				break
	return dominatedLabels
    
"""




def dominate(labelList):
    dominatedLabels = []
    lastLabel = labelList[-1]

    # Loop over all labels except the last one
    for i, label in enumerate(labelList[:-1]):
        # Check if the last visited node in detailedPath is the same for both labels
        if label.detailedPath[-1] == lastLabel.detailedPath[-1]: # Make sure to not dominate intermediate nodes that have travelled further, but share the same last intermediate node
            # Compare all attributes except 'elem'
            last_attrs = (lastLabel.time, lastLabel.timeToNext, lastLabel.drive_R, lastLabel.drive_B, lastLabel.elapsed_R)
            current_attrs = (label.time, label.timeToNext, label.drive_R, label.drive_B, label.elapsed_R)

            # Separate comparison for 'elem' if it exists
            elem_comparison = True  # Default to True if 'elem' attribute doesn't exist
            if hasattr(lastLabel, 'elem') and hasattr(label, 'elem'):
                elem_comparison = np.array_equal(np.asarray(lastLabel.elem), np.asarray(label.elem))

            # Apply domination logic
            if all(l == c for l, c in zip(last_attrs, current_attrs)) and elem_comparison:
                lastLabel.done = True
                dominatedLabels.append(len(labelList) - 1)
                break
            elif all(l <= c for l, c in zip(last_attrs, current_attrs)) and (not hasattr(lastLabel, 'elem') or np.all(np.asarray(lastLabel.elem) <= np.asarray(label.elem))):
                if not label.done:
                    label.done = True
                    dominatedLabels.append(i)
            elif all(l >= c for l, c in zip(last_attrs, current_attrs)) and (not hasattr(lastLabel, 'elem') or np.all(np.asarray(lastLabel.elem) >= np.asarray(label.elem))):
                lastLabel.done = True
                dominatedLabels.append(len(labelList) - 1)
                break
        else:
            # If the last visited nodes are different, no domination is possible
            continue

    return dominatedLabels
