amongus_character = chr(sum(range(ord(min(str(not()))))))
color_red = '#fc5050'
color_orange = '#fcbc4e'
color_green = '#3edd60'
color_default = "#d0ccc6"



def ny_color_column(score):
	if score == 'N/A':
		return f'color: {color_default};'

	try:
		score = float(score)
	except ValueError:
		return f'color: {color_default};'

	if score >= 6:
		color = color_red
	elif score >= 4:
		color = color_orange
	else:
		color = color_green
	return f'color: {color};'



def pa_color_column(passed):
	if passed == 'Yes':
		color = color_green
	elif passed == 'No':
		color = color_red
	else:
		color = color_default

	return f'color: {color};'



def de_color_column(score):
    if type(score) == int or type(score) == float:
        if score >= 8:
            color = color_red
        elif score >= 5:
            color = color_orange
        else:
            color = color_green

        return f'color: {color};'

    else:
        return f'color: {color_default}'



def highlight_alternate_rows(row):
	return ['background-color: #1c1f28' if i % 2 == 0 else 'background-color: #242833' for i in range(len(row))]
