// https://developers.google.com/apps-script/reference/forms
function newSimpleForm() {
    var form = FormApp.create('2020.06.27 Математический марафон');
    form.setDescription('Условия участия и задачи:\nhttps://notion.so/Math-Marathon-8acf3ff3b2874cefabbfa78d2db4f07e');
    form.setConfirmationMessage('Спасибо за участие, ты молодец! Результаты будут в течение недели (стараемся быстрее, но обещать не можем).');
    form.setShowLinkToRespondAgain(false);
    form.setPublishingSummary(false);  // default

    var nameItem = form.addTextItem();
    nameItem.setTitle('Имя Фамилия');
      
    var classItem = form.addMultipleChoiceItem();
    classItem.setTitle('Класс (на сентябрь 2020 г.)')
        .setChoices([
            classItem.createChoice(8),
            classItem.createChoice(9),
            classItem.createChoice(10),
            classItem.createChoice(11),
        ])
        .showOtherOption(true);

    var schoolItem = form.addMultipleChoiceItem();
    schoolItem.setTitle('Школа (на сентябрь 2020 г.)')
        .setChoices([
            schoolItem.createChoice('554, Москва'),
        ])
        .showOtherOption(true);
      
    var counts = [8, 18, 8];
    for (const [partIndex, partSize] of counts.entries()) {
        var part = partIndex + 1;
        var title = part.toString() + '.1–' + part.toString() + '.' + partSize.toString();
        Logger.log('title ' + title);
        var item = form.addSectionHeaderItem();
        item.setTitle(title);
        
        for (const problemIndex of Array(partSize).keys()) {
            var problem = part.toString() + '.' + (problemIndex + 1).toString();
            var item = form.addTextItem();  // short text
            item.setTitle(problem);
        }
    }

    var item = form.addSectionHeaderItem();
    item.setTitle('Это конец формы, пора всё проверить и отправлять');
    Logger.log('Done: ' + form.getEditUrl());
}
