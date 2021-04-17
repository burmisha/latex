import logging
log = logging.getLogger(__name__)


class GoogleForm:
    def __init__(
        self,
        title=None,
        description=None,
        confirmationMessage=None,
        showLinkToRespondAgain=False,
        linkNewSpreadsheet=False,
        link_existing=None,
    ):
        showLinkToRespondAgain = str(showLinkToRespondAgain).lower()
        self._query = f'''
            var form = FormApp.create('{title}');
            form.setDescription('{description}');
            form.setConfirmationMessage('{confirmationMessage}');
            form.setShowLinkToRespondAgain({showLinkToRespondAgain});
            form.setPublishingSummary(false);  // default
'''

        if linkNewSpreadsheet and link_existing:
            raise RuntimeError(f'Could not set two destinations: {linkNewSpreadsheet} {link_existing}')

        if linkNewSpreadsheet:
            self._query += f'''
            var ss = SpreadsheetApp.create('{title} - ответы');
            form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
'''

        if link_existing:
            self._query += f'''
            var ss = SpreadsheetApp.openById("{link_existing}");
            form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
            // ss.getSheets()[0].setName('SOME NAME');
'''
        self._item_id = 0

    def _get_new_id(self):
        self._item_id += 1
        return 'item_%d' % self._item_id

    def _to_json_bool(self, value):
        return str(value).lower()

    def AddTextItem(self, title=None, helpText=None, required=False):
        iid = self._get_new_id()
        required = self._to_json_bool(required)
        self._query += f'''
            var {iid} = form.addTextItem();
            {iid}.setTitle('{title}')
            {iid}.setRequired({required});
'''
        if helpText:
            self._query += f'''            {iid}.setHelpText('{helpText}');\n'''

    def AddMultipleChoiceItem(self, title=None, choices=None, showOtherOption=False):
        iid = self._get_new_id()
        choicesStr = ',\n                    '.join(['''{}.createChoice('{}')'''.format(iid, choice) for choice in choices])
        showOtherOption = self._to_json_bool(showOtherOption)
        self._query += f'''
            var {iid} = form.addMultipleChoiceItem();
            {iid}.setTitle('{title}')
                .setChoices([
                    {choicesStr}
                ])
                .showOtherOption({showOtherOption});
'''

    def AddSectionHeaderItem(self, title=None):
        iid = self._get_new_id()
        self._query += f'''
            var {iid} = form.addSectionHeaderItem();
            {iid}.setTitle('{title}');
'''

    def AddImageItem(self, url=None, title=None, helpText=None):
        iid = self._get_new_id()
        self._query += f'''
            var {iid} = UrlFetchApp.fetch('{url}');
            form.addImageItem()
            .setTitle('{title}')
            .setHelpText('{helpText}') // The help text is the image description
            .setImage({iid})
        '''
        # TODO: add .setAlignment(form.Alignment.CENTER);

    def FormQuery(self):
        query = f'''
function newSimpleForm(){{{self._query}
    Logger.log('Done: ' + form.getEditUrl());
}}'''
        return query
