def extract_special_offer(soup):

    for p in soup.find_all("p"):

        classes = p.get("class", [])
        text = p.get_text(" ", strip=True)

        if (
            "has-vivid-red-color" in classes
            and text.upper().startswith("SPECIAL OFFER")
        ):
            return text

    return None