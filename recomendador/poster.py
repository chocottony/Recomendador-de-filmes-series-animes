if item_image:
    html_content += f'<div><img src="https://image.tmdb.org/t/p/w500{item_image}" alt="{item_name}"> <p>{item_name} - {item_overview}</p></div>' 
else:
    html_content += f'<div><img src="https://placehold.co/400?text=No+Image+Available" alt="{item_name}"> <p>{item_name} - {item_overview}</p></div>'