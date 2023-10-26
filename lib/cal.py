"""Calendar"""
import os
import json
import logging
import webbrowser
from lib import fndate


class CalendarExport:
    """Calendar"""
    def __init__(self, dist_dir, prices):
        self.dist_dir = dist_dir
        self.prices = prices
        self.d = {
            "start": fndate.date_format(prices.start()),
            "end": fndate.date_format(prices.end())
        }

    def leaves(self, prices):
        """Leaf nodes"""
        leaves = []
        for child in prices.get_children():
            if child.is_leaf():
                leaves.append(child)
            else:
                leaves.extend(self.leaves(child))
        return leaves

    def to_json(self):
        """To JSON"""
        leaves = self.leaves(self.prices)
        self.d["days"] = []
        for leaf in leaves:
            self.d["days"].append({
                "start": fndate.date_format(leaf.start()),
                "end": fndate.date_format(leaf.end()),
                "price": leaf.price(),
                "descr": leaf.description(),
                "type": leaf.type()
            })
        with open(os.path.join(self.dist_dir, 'data.js'), 'w', encoding='utf-8') as f:
            logging.debug("write to %s", os.path.join(self.dist_dir, 'data.js'))
            f.write("const data = ")
            json.dump(self.d, f)
            webbrowser.open(f"file://{os.path.realpath(os.path.join(self.dist_dir, 'index.html'))}", new=2)

# ~@:-]
