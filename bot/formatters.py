
def format_listing(listing):
    text = (
        f"{listing['address']}\n"
        f"Rating: {listing['rating']}/10\n"
        f"Price: ${listing['price']:,}\n"
        f"Distance: {listing['distance_miles']} mi from campus\n\n"
        f"{listing['summary']}\n\n"
        f"{listing['details']}"
    )
    return text