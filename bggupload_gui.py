# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 28 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.xrc

###########################################################################
## Class mainframe
###########################################################################

class mainframe ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 775,374 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		searchboxChoices = []
		self.searchbox = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, searchboxChoices, wx.TE_PROCESS_ENTER )
		bSizer5.Add( self.searchbox, 1, wx.ALL, 0 )
		
		searchtypeChoices = [ u"UPC Auto", u"UPC", u"Text" ]
		self.searchtype = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, searchtypeChoices, 0 )
		self.searchtype.SetSelection( 0 )
		bSizer5.Add( self.searchtype, 0, wx.ALL, 0 )
		
		
		bSizer6.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		self.infolink = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"BGG Website", u"https://www.boardgamegeek.com/", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		self.infolink.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.infolink.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer6.Add( self.infolink, 0, wx.ALL|wx.EXPAND, 2 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.mainwindow = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.mainwindow.SetScrollRate( 5, 5 )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.mainwindow.SetSizer( bSizer7 )
		self.mainwindow.Layout()
		bSizer7.Fit( self.mainwindow )
		bSizer61.Add( self.mainwindow, 10, wx.EXPAND |wx.ALL, 5 )
		
		self.importlist = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.importlist.SetScrollRate( 5, 5 )
		importlistsizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.importlist.SetSizer( importlistsizer )
		self.importlist.Layout()
		importlistsizer.Fit( self.importlist )
		bSizer61.Add( self.importlist, 3, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer61, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		self.status = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		self.m_menubar2 = wx.MenuBar( 0 )
		self.m_menu2 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Paste From Clipboard", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem1 )
		
		self.m_menuItem2 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"From File", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem2 )
		
		self.m_menubar2.Append( self.m_menu2, u"Load" ) 
		
		self.m_menu31 = wx.Menu()
		self.tofile = wx.MenuItem( self.m_menu31, wx.ID_ANY, u"To File (Toggle)", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu31.Append( self.tofile )
		self.tofile.Check( True )
		
		self.tobgg = wx.MenuItem( self.m_menu31, wx.ID_ANY, u"To BGG (Toggle)", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu31.Append( self.tobgg )
		
		self.m_menubar2.Append( self.m_menu31, u"Save" ) 
		
		self.m_menu5 = wx.Menu()
		self.m_menuItem7 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Output", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem7 )
		
		self.m_menubar2.Append( self.m_menu5, u"View" ) 
		
		self.m_menu4 = wx.Menu()
		self.m_menuItem6 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Remove Selected (green) Row", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem6 )
		
		self.fuzzysearch = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Fuzzy Local Search", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menu4.Append( self.fuzzysearch )
		self.fuzzysearch.Check( True )
		
		self.m_menubar2.Append( self.m_menu4, u"Edit" ) 
		
		self.m_menu3 = wx.Menu()
		self.m_menuItem3 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"About...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.Append( self.m_menuItem3 )
		
		self.m_menubar2.Append( self.m_menu3, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.searchbox.Bind( wx.EVT_TEXT_ENTER, self.Search )
		self.searchtype.Bind( wx.EVT_CHOICE, self.OnSearch )
		self.Bind( wx.EVT_MENU, self.Paste, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.ImportFile, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.export_to_file, id = self.tofile.GetId() )
		self.Bind( wx.EVT_MENU, self.export_to_bgg, id = self.tobgg.GetId() )
		self.Bind( wx.EVT_MENU, self.ShowOutputPanel, id = self.m_menuItem7.GetId() )
		self.Bind( wx.EVT_MENU, self.RemoveRow, id = self.m_menuItem6.GetId() )
		self.Bind( wx.EVT_MENU, self.FuzzySearchEnable, id = self.fuzzysearch.GetId() )
		self.Bind( wx.EVT_MENU, self.About, id = self.m_menuItem3.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Search( self, event ):
		event.Skip()
	
	def OnSearch( self, event ):
		event.Skip()
	
	def Paste( self, event ):
		event.Skip()
	
	def ImportFile( self, event ):
		event.Skip()
	
	def export_to_file( self, event ):
		event.Skip()
	
	def export_to_bgg( self, event ):
		event.Skip()
	
	def ShowOutputPanel( self, event ):
		event.Skip()
	
	def RemoveRow( self, event ):
		event.Skip()
	
	def FuzzySearchEnable( self, event ):
		event.Skip()
	
	def About( self, event ):
		event.Skip()
	

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel3.SetSizer( bSizer9 )
		self.m_panel3.Layout()
		bSizer9.Fit( self.m_panel3 )
		bSizer8.Add( self.m_panel3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_panel4.Bind( wx.EVT_KILL_FOCUS, self.KillFocusImage )
		self.m_panel4.Bind( wx.EVT_SET_FOCUS, self.SetFocusImage )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def KillFocusImage( self, event ):
		event.Skip()
	
	def SetFocusImage( self, event ):
		event.Skip()
	

###########################################################################
## Class helpdialog
###########################################################################

class helpdialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 909,638 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.helptextbox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		bSizer8.Add( self.helptextbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class ColumnMatcher
###########################################################################

class ColumnMatcher ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 798,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.ColumnsExportList = wx.ListCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer13.Add( self.ColumnsExportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer13 )
		self.m_panel4.Layout()
		bSizer13.Fit( self.m_panel4 )
		bSizer9.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel41 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer131 = wx.BoxSizer( wx.VERTICAL )
		
		self.ColumnsImportList = wx.ListCtrl( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer131.Add( self.ColumnsImportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel41.SetSizer( bSizer131 )
		self.m_panel41.Layout()
		bSizer131.Fit( self.m_panel41 )
		bSizer9.Add( self.m_panel41, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button1 = wx.Button( self.m_panel3, wx.ID_ANY, u"Match", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self.m_panel3, wx.ID_ANY, u"< Unmatch", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.ColumnsMatchList = wx.ListCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer10.Add( self.ColumnsMatchList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer10 )
		self.m_panel3.Layout()
		bSizer10.Fit( self.m_panel3 )
		bSizer9.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ColumnsExportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsExportList.Bind( wx.EVT_SIZE, self.resize )
		self.ColumnsImportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsImportList.Bind( wx.EVT_SIZE, self.resize )
		self.m_button1.Bind( wx.EVT_BUTTON, self.match )
		self.m_button2.Bind( wx.EVT_BUTTON, self.unmatch )
		self.ColumnsMatchList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.unmatch )
		self.ColumnsMatchList.Bind( wx.EVT_SIZE, self.resize )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def match( self, event ):
		event.Skip()
	
	def resize( self, event ):
		event.Skip()
	
	
	
	
	def unmatch( self, event ):
		event.Skip()
	
	
	

