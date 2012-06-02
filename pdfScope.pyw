import wx, subprocess, os

# TODO: Refrencing via pdf-parser
# TODO: Scrollbars
# TODO: Selectable Text
# TODO: Better viewers for hex, strings and filtered views
# TODO: Progress bar / busy msg whilst loading PDF
# TODO: Search term highlighting
# TODO: JavaScript beautifier
# TODO: SpiderMonkey support
# TODO: Malzilla link


class Page(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class MainFrame(wx.Frame):
    
    def __init__(self):
        
        wx.Frame.__init__(self, None,title="PDFView v0.5 by Frank J Bruzzaniti (frank.bruzzaniti@gmail.com)",size=(1200, 600))

        menubar = wx.MenuBar() 

        # Create File menu
        fileMenu = wx.Menu()        
        menubar.Append(fileMenu, '&File')
        fileItem = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open PDF')
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnQuit,id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpen,id=wx.ID_OPEN)

        # Create Object menu
        objectMenu = wx.Menu()
        viewItem = objectMenu.Append(wx.NewId(), 'View', 'View Object')
        saveItem = objectMenu.Append(wx.NewId(), 'Save', 'Save Object')
        menubar.Append(objectMenu, '&Object')
        self.Bind(wx.EVT_MENU, self.objDialog,viewItem)

        # Create View menu
        objectMenu = wx.Menu()
        pdfItem = objectMenu.Append(wx.NewId(), 'Filtered Text', 'View Filtered PDF')
        hexItem = objectMenu.Append(wx.NewId(), 'Hexadecimal', 'View PDF as Hex')
        stringsItem = objectMenu.Append(wx.NewId(), 'Extracted Strings', 'View extracted strings')
        menubar.Append(objectMenu, '&View PDF')
        self.Bind(wx.EVT_MENU, self.viewFiltered,pdfItem)
        self.Bind(wx.EVT_MENU, self.viewHex,hexItem)
        self.Bind(wx.EVT_MENU, self.viewStrings,stringsItem)

        
        self.SetMenuBar(menubar)
                                
        # Create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        self.pdf_path = ''  

        # create the page windows as children of the notebook
        self.page1 = Page(nb)
        self.page2 = Page(nb)
        self.page3 = Page(nb)
        self.page4 = Page(nb)
        self.page5 = Page(nb)
        self.page6 = Page(nb)
        self.page7 = Page(nb)
        self.page8 = Page(nb)
        self.page9 = Page(nb)
        self.page10 = Page(nb)
        self.page11 = Page(nb)
        self.page12 = Page(nb)
       
        
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "PDFiD")
        nb.AddPage(self.page2, "/Page")
        nb.AddPage(self.page3, "/Encrypt")
        nb.AddPage(self.page4, "/ObjStm")
        nb.AddPage(self.page5, "/JS")
        nb.AddPage(self.page6, "/JavaScript")
        nb.AddPage(self.page7, "/AA")
        nb.AddPage(self.page8, "/OpenAction")
        nb.AddPage(self.page9, "/AcroForm")
        nb.AddPage(self.page10, "/JBIG2Decode")
        nb.AddPage(self.page11, "/RichMedia")
        nb.AddPage(self.page12, "/Launch")
        
                
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

            
    def OnQuit(self, e):
        self.Close()

    # Ask user for obj number to view    
    def objDialog(self, event):
        dlg = wx.TextEntryDialog(self, 'Enter the object number you wish to view')
        if dlg.ShowModal() == wx.ID_OK:
            print self.viewObject(dlg.GetValue())
            dlg.Destroy() 
    
    # On open of file, run scripts and display results
    def OnOpen(self, e):
        t = wx.StaticText(self.page1, -1, 'Please wait whilst I parse your PDF ... this could take a minute', (20,20))
        fileType = "PDF File (.pdf)|*.pdf"
        dialog = wx.FileDialog(None,'Choose a file',os.getcwd(),"", fileType,wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.pdf_path = dialog.GetPath()
            self.PDFiD()
            t = wx.StaticText(self.page2, -1, self.pdf_parser('/Page'), (20,20))
            t = wx.StaticText(self.page3, -1, self.pdf_parser('/Encrypt'), (20,20))
            t = wx.StaticText(self.page4, -1, self.pdf_parser('/ObjStm'), (20,20))
            t = wx.StaticText(self.page5, -1, self.pdf_parser('/JS'), (20,20))
            t = wx.StaticText(self.page6, -1, self.pdf_parser('/JavaScript'), (20,20))
            t = wx.StaticText(self.page7, -1, self.pdf_parser('/AA'), (20,20))
            t = wx.StaticText(self.page8, -1, self.pdf_parser('/OpenAction'), (20,20))
            t = wx.StaticText(self.page9, -1, self.pdf_parser('/AcroForm'), (20,20))
            t = wx.StaticText(self.page10, -1, self.pdf_parser('/JBIG2Decode'), (20,20))
            t = wx.StaticText(self.page11, -1, self.pdf_parser('/RichMedia'), (20,20))
            t = wx.StaticText(self.page12, -1, self.pdf_parser('/Launch'), (20,20))
            
            
        dialog.Destroy()
        
    # runs PDFiD.py and checksums.py
    def PDFiD(self):
        pr1 = subprocess.Popen('pdfid.py ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        pr2 = subprocess.Popen('checksums.py ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr1.stdout.readlines():
            lst_results.append(line)
        for line in pr2.stdout.readlines():
            lst_results.append(line)
        #retval = pr.wait()
        t = wx.StaticText(self.page1, -1, ''.join(lst_results), (20,20))

    # Runs pdf-parser.py with search argument and returns console output
    def pdf_parser(self, query):
        pr = subprocess.Popen('pdf-parser.py --search ' + query + ' ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr.stdout.readlines():
            lst_results.append(line)
        return ''.join(lst_results)

    # Runs pdf-parser extracting object with pdf-parser -f --raw -o
    def viewObject(self, obj_num):
        pr = subprocess.Popen('pdf-parser.py -f --raw -o ' + obj_num + ' ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr.stdout.readlines():
            lst_results.append(line)
        return ''.join(lst_results)

    # Runs pdf-parser extracting filtered text with pdf-parser -f --raw
    def viewFiltered(self, e):
        pr = subprocess.Popen('pdf-parser.py -f --raw ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr.stdout.readlines():
            lst_results.append(line)
        print ''.join(lst_results)

    # Runs hex.py displaying pdf in hex
    def viewHex(self, e):
        pr = subprocess.Popen('hexdump.py ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr.stdout.readlines():
            lst_results.append(line)
        print ''.join(lst_results)

    # Runs hex.py displaying pdf in hex
    def viewStrings(self, e):
        pr = subprocess.Popen('stringdump.py ' + self.pdf_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lst_results = []
        for line in pr.stdout.readlines():
            lst_results.append(line)
        print ''.join(lst_results)



if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
