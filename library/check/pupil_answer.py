from library.logging import color


class PupilAnswer:
    def __init__(self, value):
        self._value = value

    def Check(self, valid_answers_list):
        self._result_max = max(ans.Value() for ans in valid_answers_list)
        self._best_answer = list(ans for ans in valid_answers_list if ans.Value() == self._result_max)[0]
        matched_values = [ans.Value() for ans in valid_answers_list if ans.IsOk(self._value)]
        if not matched_values:
            self._result = 0
        else:
            self._result = matched_values[0]

        current_color = None
        best_color = None
        if self._result == self._result_max:
            current_color = color.Green
        else:
            if self._result > 0:
                current_color = color.Yellow
            else:
                current_color = color.Red

            if self._value and len(self._best_answer.Printable()) >= 2:
                best_color = color.Cyan

        self._color = current_color
        self._best_color = best_color
