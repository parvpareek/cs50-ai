import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    sum = 0
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        sum += ranks[page]
    ranks = iterate_pagerank(corpus, DAMPING)
    print(sum)
    print(f"PageRank Results from Iteration")
    sum = 0
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
        sum += ranks[page]
    print(sum)



def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:  
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Get the set of all pages given page links to 
    links = corpus[page]
    distribution = {}

    # If it links to 0 pages
    if len(links) == 0:
        for page in corpus:
            distribution[page] = (1/len(corpus))
        return distribution
    

    

    for each_page in corpus:
        probability = 0
        if each_page in links:
            probability = damping_factor/len(links)
        probability = probability + (1 - damping_factor)/len(corpus)
        distribution[each_page] = probability

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    track = {}
    for each_page in corpus:
        track[each_page] = 0

    page = random.choice(list(corpus.keys()))
    track[page] = track[page] + 1
    

    for i in range(n):
            transition_distribution = transition_model(corpus, page, damping_factor)
            weights = list(transition_distribution.values())
            population = list(transition_distribution.keys())
            page_list = random.choices(population, weights, k=1)
            page = page_list[0]
            track[page] = track[page] + 1

    page_rank = {}

    for page in corpus:
        page_rank.update({page: track[page]/n})
    
    return page_rank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.    
    """

    dict = {}
    page_rank = {}
    N = len(corpus)

    # Iterate through every page in the corpus
    for page in corpus:
        # Set the page rank of each page to a default value
        page_rank[page] = 1/N

        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())

        # Find all the pages that to link to the current page in the loop and map it in the dictionary
        linked_by = set()
        
        # Create a set of pages that link to the current page
        for each_page in corpus:
            if page == each_page:
                continue
            if page in corpus[each_page] or len(corpus[each_page])== 0:
                linked_by.add(each_page)
        # Map the set to the current poage in a dictionary
        dict[page] = linked_by
    
    while True:
        converged = True
        # For every page in the corpus
        for page in corpus:
            
            # First term of the equation which is a constant
            pr = (1 - damping_factor)/N

            # Loop through every page that links to the current page
            for linked_page in dict[page]:
                # Add the remaining terms which is the pagerank of the linking page divided by the number of links present in the linking page
                num_links = len(corpus[linked_page])
                pr +=  damping_factor*(page_rank[linked_page]/num_links)

            
            difference = abs(page_rank[page] - pr)

            if difference > 0.001:
                converged = False
                page_rank[page] = pr
        if converged:
            return page_rank




if __name__ == "__main__":
    main()
