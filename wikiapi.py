import wikipedia as wiki

def main():
    wiki.set_lang("nl")

    r_pages = [wiki.random(1) for i in range(10)]
    for p in r_pages:
        try:
            summary = wiki.page(p).summary
        except:
            p = wiki.suggest(p)
            summary = wiki.page().summary
        print (f"{p}\n\n{summary}\n")

if __name__ == "__main__":
    main()
