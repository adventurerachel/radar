import re


def extract_barclaycard_bonus(soup):

    elements = soup.find_all(["h2", "h3", "p"])

    paragraphs = [
        element.get_text(" ", strip=True)
        for element in elements
    ]

    bonus_avios = None
    spend_requirement = None

    target_heading = (
        "what is the barclaycard avios plus mastercard sign-up bonus?"
    )

    for index, text in enumerate(paragraphs):

        #if "sign-up bonus" in text.lower():
        #    print(index, repr(text))

        if target_heading in text.lower().strip():

            following_text = " ".join(
                paragraphs[index:index + 5]
            )

            avios_match = re.search(
                r"([\d,]+)\s+Avios",
                following_text,
                re.IGNORECASE,
            )

            if avios_match:
                bonus_avios = int(
                    avios_match.group(1).replace(",", "")
                )

            spend_match = re.search(
                r"£\s?([\d,]+)",
                following_text,
            )

            if spend_match:
                spend_requirement = int(
                    spend_match.group(1).replace(",", "")
                )

            break

    return {
        "bonus_avios": bonus_avios,
        "spend_requirement_gbp": spend_requirement,
    }