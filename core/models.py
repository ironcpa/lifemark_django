

class LifemarkLineSearchData():
    def __init__(self, field, line_no, match_line):
        self.field = field
        self.line_no = line_no
        self.match_line = match_line


class LifemarkLineListData():
    def __init__(self, lifemark, lines):
        self.lifemark = lifemark
        self.lines = lines
