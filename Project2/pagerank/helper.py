from pagerank import transition_model, sample_pagerank

corpussy = {
    "1.html": ("2.html", "3.html"),
    "2.html": ("3.html"),
    "3.html": ("2.html")
}
pg = "1.html"
print(sample_pagerank(corpussy, 0.85, 10000))