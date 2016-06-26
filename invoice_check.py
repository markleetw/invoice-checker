#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from Tkinter import *
import json
import tkMessageBox


class InvoiceChecker(Frame):
    url = 'http://invoice.etax.nat.gov.tw'
    invoice_data = list()
    current_invoice_data = dict()
    valid_input = '0123456789'
    succ_invoice = ''
    is_special = False
    award = ['0', '0', '200', '1,000', '4,000', '10,000', '40,000', '200,000', '2,000,000', '10,000,000']

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.getInvoiceData()
        self.createWidgets()

    def getInvoiceData(self):
        """
        get the latest two period invoice data
        """
        period = [0, 1]  # period: 0 means the latest period, and 1 is last period
        html = urllib2.urlopen(self.url).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = list()
        for p in period:
            area_id = 'area' + str(p + 1)
            area = soup.find('div', id=area_id)
            title = unicode(area.find_all('h2')[1].string)
            span_list = area.table.find_all('span')
            invoice_nums = list()
            amount_of_awards = [0, 0, 0, 0]  # 特別獎、特獎、頭獎、六獎
            count = 0
            for i in span_list:
                span_str = i.string
                num_list = span_str.split(u'、')
                for num in num_list:
                    invoice_nums.append(str(num))
                    amount_of_awards[count] += 1
                count += 1
            data.append({'title': title, 'invoice_nums': invoice_nums, 'amount': amount_of_awards})
        self.invoice_data = data
        self.current_invoice_data = data[0]

    def selectTheLatestPeriod(self):
        self.current_invoice_data = self.invoice_data[0]
        self.succ_invoice = ''
        self.is_special = False
        self.displayInvoiceText()
        self.clearInput()

    def selectTheSecondLastPeriod(self):
        self.current_invoice_data = self.invoice_data[1]
        self.succ_invoice = ''
        self.is_special = False
        self.displayInvoiceText()
        self.clearInput()

    def displayInvoiceText(self):
        invoices = self.current_invoice_data['invoice_nums']
        amount = self.current_invoice_data['amount']
        self.invoiceText['text'] = self.current_invoice_data['title'] + \
                                   u'\n特別獎: ' + ', '.join(str(e) for e in invoices[:amount[0]]) + \
                                   u'\n特獎: ' + ', '.join(str(e) for e in invoices[amount[0]:amount[0] + amount[1]]) + \
                                   u'\n頭獎: ' + ', '.join(str(e) for e in invoices[amount[0] + amount[1]:-amount[3]]) + \
                                   u'\n六獎: ' + ', '.join(str(e) for e in invoices[-amount[3]:])

    def inputKeyRelease(self, event):
        input_text = self.inputField.get()
        if event.char in self.valid_input:
            real_invoice = input_text[::-1]
            input_len = len(real_invoice)
            succ = False
            for idx, invoice_num in enumerate(self.current_invoice_data['invoice_nums']):
                if len(invoice_num) >= input_len:
                    if invoice_num[0 - input_len:] == real_invoice:
                        succ = True
                        self.succ_invoice = real_invoice
                        if idx in [0, 1]:  # 判斷是否為特獎/特別獎
                            self.is_special = True
                        else:
                            self.is_special = False

            if not succ:
                if len(self.succ_invoice) in range(3, 8) and not self.is_special:  # 特別獎和特獎只有全中才算數
                    tkMessageBox.showinfo('貪財貪財', '尾數為「' + self.succ_invoice + '」超爽der，撿到 %s 塊！' % self.award[
                        len(self.succ_invoice) - 1])
                else:
                    tkMessageBox.showerror('槓龜', '很抱歉，尾數為「%s」的發票沒有中獎' % real_invoice)
                self.succ_invoice = ''
                self.is_special = False
                self.clearInput()
            elif len(self.succ_invoice) == 8:
                award = ''
                invoices = self.current_invoice_data['invoice_nums']
                amount = self.current_invoice_data['amount']
                if self.succ_invoice in invoices[:amount[0]]:
                    award = self.award[-1]
                elif self.succ_invoice in invoices[amount[0]:amount[0] + amount[1]]:
                    award = self.award[-2]
                else:
                    award = self.award[-3]
                tkMessageBox.showinfo('發財啦！', '發票號碼 「' + self.succ_invoice + '」發達啦！中大獎 %s 元！' % award)
                self.succ_invoice = ''
                self.is_special = False
                self.clearInput()

    def validateInput(self, action, index, value_if_allowed,
                      prior_value, text, validation_type, trigger_type, widget_name):
        if text in self.valid_input:
            return True
        else:
            return False

    def clearInput(self):
        # sometimes delete to end doesn't work
        self.inputField.delete(0, END)
        self.succ_invoice = ''
        self.is_special = False
        finished = False
        while finished is False:
            self.inputField.delete(0)
            finished = len(self.inputField.get()) == 0

    def createWidgets(self):
        """
        create gui widgets
        """
        # switch invoice period (the latest and the second last periods)
        self.latest_btn = Button(self, command=self.selectTheLatestPeriod)
        self.latest_btn["text"] = self.invoice_data[0]['title']
        self.latest_btn.grid(row=0, column=0)

        self.sec_last_btn = Button(self, command=self.selectTheSecondLastPeriod)
        self.sec_last_btn["text"] = self.invoice_data[1]['title']
        self.sec_last_btn.grid(row=0, column=6)

        # display all invoice info of selected period
        self.invoiceText = Label(self)
        self.invoiceText.grid(row=1, column=0, columnspan=7)
        self.displayInvoiceText()

        # input field
        self.inputText = Label(self)
        self.inputText['text'] = u'輸入: '
        self.inputText.grid(row=2, column=0)
        vcmd = (self.register(self.validateInput),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.inputField = Entry(self, validate='key', validatecommand=vcmd)
        self.inputField['width'] = 50
        self.inputField.grid(row=2, column=1, columnspan=5)
        self.inputField.bind('<KeyRelease>', self.inputKeyRelease)
        self.inputField.focus()
        self.clear_btn = Button(self, command=self.clearInput)
        self.clear_btn["text"] = '清空'
        self.clear_btn.grid(row=2, column=6)

        # display readme
        self.descText = Label(self)
        self.descText.grid(row=3, column=0, columnspan=7)
        self.descText['text'] = u'說明: 請將發票號碼倒著輸入(由右至左)！'


if __name__ == '__main__':
    root = Tk()
    root.title('統一發票對獎器')
    app = InvoiceChecker(master=root)
    app.mainloop()
