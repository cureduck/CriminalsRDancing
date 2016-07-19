cards=('dog','criminal','f_responder','common_ones','detective','info_swap','trade','rumour','alibi','unknown','witness')
class card():
    def __init__(self,name='unknown'):
        self._name=name

    @property
    def name(self):
        return self._name



c=card()

