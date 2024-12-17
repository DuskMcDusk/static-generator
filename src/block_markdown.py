def markdown_to_blocks(markdown):
    return list(filter(
            lambda y: y != "",
            map(lambda x: x.strip(),
                markdown.split("\n\n"))))

def block_to_block_type(block):
    if block.startswith("#"):
        return "heading"
    if block.startswith("```"):
        return "code"
    lines = block.split("\n")

    filter_quote = list(filter(lambda x: x.startswith(">"), lines))
    if len(filter_quote) == len(lines):
        return "quote"
    filter_unordered_list = list(filter(
        lambda x: x.startswith("* ") or x.startswith("- "), lines))
    if len(filter_unordered_list) == len(lines):
        return "unordered"
    
    isordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}."):
            isordered = False
            break
    if isordered: return "ordered"

    return "paragraph"
