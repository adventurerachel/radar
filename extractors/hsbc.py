def extract_hsbc_conclusion(soup):

    heading = soup.find(
        "h2",
        string=lambda x:
            x and x.strip().lower() == "conclusion"
    )

    if not heading:
        return None

    paragraph = heading.find_next("p")

    if not paragraph:
        return None

    return paragraph.get_text(
        " ",
        strip=True
    )