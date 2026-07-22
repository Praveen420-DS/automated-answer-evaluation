from app.ocr.benchmark import ground_truth_pairs, similarity_metrics


def test_ground_truth_pairs_match_every_sample():
    pairs = ground_truth_pairs()

    assert len(pairs) == 7
    assert {image.stem for image, _ in pairs} == {
        "Closest10",
        "Closest12",
        "Closest13",
        "Listman15",
        "Listman16",
        "Listman17",
        "Listman2",
    }


def test_similarity_metrics_are_separate_and_weighted():
    metrics = similarity_metrics("alpha beta", "alpha gamma")

    assert 0 < metrics["character_similarity"] < 1
    assert metrics["token_similarity"] == 1 / 3
    assert metrics["overall_similarity"] == (
        0.7 * metrics["character_similarity"]
    ) + (0.3 / 3)
