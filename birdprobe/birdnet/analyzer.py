from birdnetlib.analyzer import Analyzer

class LiveAnalyzer(Analyzer):
    def __init__(self, *args, **kwargs):
        super(Analyzer, self).__init__(*args, **kwargs)

    def analyze_live(self, chunk):
        pred = self.predict(chunk)[0]

        # Assign scores to labels
        p_labels = dict(zip(self.labels, pred))

        # Sort by score
        p_sorted = sorted(
            p_labels.items(), key=operator.itemgetter(1), reverse=True
        )

        # Return results
        return p_sorted
