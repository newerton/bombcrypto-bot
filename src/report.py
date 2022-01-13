from pathlib import Path

import csv


class Report:
    def openFile(self, file, headers=False):
        path = Path(file)
        if path.is_file() is False:
            f = open(file, 'a', encoding='UTF8', newline='')
            if headers is not False:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(headers)
        else:
            f = open(file, 'a', encoding='UTF8', newline='')
        return f

    def writeCsv(self, filename, headers, content):
        file = self.openFile('./reports/{}.csv'.format(filename), headers)
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(content)
        file.close()
        print(file)
