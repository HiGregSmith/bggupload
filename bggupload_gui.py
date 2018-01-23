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
## Class ColumnMatcherFrame
###########################################################################

class ColumnMatcherFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 798,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		ListsSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ColumnsExportList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer2.Add( self.ColumnsExportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.ColumnsImportList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer2.Add( self.ColumnsImportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.ColumnsMatchList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer2.Add( self.ColumnsMatchList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( ListsSizer2 )
		self.Layout()
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Load", wx.Bitmap( u"icons/Open-file-icon.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool2 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Save", wx.Bitmap( u"icons/Save-as-icon32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool3 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Match", wx.Bitmap( u"icons/equal-mathematical-sign.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool4 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Unmatch", wx.Bitmap( u"icons/is-not-equal-to-mathematical-symbol.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ColumnsExportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsExportList.Bind( wx.EVT_SIZE, self.resize )
		self.ColumnsImportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsImportList.Bind( wx.EVT_SIZE, self.resize )
		self.ColumnsMatchList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.unmatch )
		self.ColumnsMatchList.Bind( wx.EVT_SIZE, self.resize )
		self.Bind( wx.EVT_TOOL, self.load, id = self.m_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.save, id = self.m_tool2.GetId() )
		self.Bind( wx.EVT_TOOL, self.match, id = self.m_tool3.GetId() )
		self.Bind( wx.EVT_TOOL, self.unmatch, id = self.m_tool4.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def match( self, event ):
		event.Skip()
	
	def resize( self, event ):
		event.Skip()
	
	
	
	def unmatch( self, event ):
		event.Skip()
	
	
	def load( self, event ):
		event.Skip()
	
	def save( self, event ):
		event.Skip()
	
	
	

###########################################################################
## Class MyDialog2
###########################################################################

class MyDialog2 ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 959,578 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ColumnsExportList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer9.Add( self.ColumnsExportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.ColumnsImportList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer9.Add( self.ColumnsImportList, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.ColumnsMatchList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer9.Add( self.ColumnsMatchList, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ColumnsExportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsExportList.Bind( wx.EVT_SIZE, self.resize )
		self.ColumnsImportList.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.ColumnsImportList.Bind( wx.EVT_SIZE, self.resize )
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
	
	

###########################################################################
## Class ColumnMatcher
###########################################################################

class ColumnMatcher ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1027,615 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel12 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Load = wx.Button( self.m_panel12, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Load.Hide()
		
		bSizer23.Add( self.Load, 0, wx.ALL, 5 )
		
		self.Save = wx.Button( self.m_panel12, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Save.Hide()
		
		bSizer23.Add( self.Save, 0, wx.ALL, 5 )
		
		self.Match = wx.Button( self.m_panel12, wx.ID_ANY, u"Match", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Match.Hide()
		
		bSizer23.Add( self.Match, 0, wx.ALL, 5 )
		
		self.Unmatch = wx.Button( self.m_panel12, wx.ID_ANY, u"Unmatch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Unmatch.Hide()
		
		bSizer23.Add( self.Unmatch, 0, wx.ALL, 5 )
		
		self.m_bpButton1 = wx.BitmapButton( self.m_panel12, wx.ID_ANY, wx.Bitmap( u"icons/Open-file-icon.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer23.Add( self.m_bpButton1, 0, wx.LEFT|wx.RIGHT, 5 )
		
		self.m_bpButton2 = wx.BitmapButton( self.m_panel12, wx.ID_ANY, wx.Bitmap( u"icons/Save-as-icon32.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer23.Add( self.m_bpButton2, 0, wx.LEFT|wx.RIGHT, 5 )
		
		self.m_bpButton3 = wx.BitmapButton( self.m_panel12, wx.ID_ANY, wx.Bitmap( u"icons/equal-mathematical-sign.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer23.Add( self.m_bpButton3, 0, wx.LEFT|wx.RIGHT, 5 )
		
		self.m_bpButton4 = wx.BitmapButton( self.m_panel12, wx.ID_ANY, wx.Bitmap( u"icons/is-not-equal-to-mathematical-symbol.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.NO_BORDER )
		bSizer23.Add( self.m_bpButton4, 0, wx.LEFT|wx.RIGHT, 5 )
		
		
		self.m_panel12.SetSizer( bSizer23 )
		self.m_panel12.Layout()
		bSizer23.Fit( self.m_panel12 )
		bSizer22.Add( self.m_panel12, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.ListsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ListsSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_listCtrl10 = wx.ListCtrl( self.ListsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer.Add( self.m_listCtrl10, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_listCtrl11 = wx.ListCtrl( self.ListsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer.Add( self.m_listCtrl11, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_listCtrl12 = wx.ListCtrl( self.ListsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		ListsSizer.Add( self.m_listCtrl12, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.ListsPanel.SetSizer( ListsSizer )
		self.ListsPanel.Layout()
		ListsSizer.Fit( self.ListsPanel )
		bSizer22.Add( self.ListsPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer22 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Load.Bind( wx.EVT_BUTTON, self.load )
		self.Save.Bind( wx.EVT_BUTTON, self.save )
		self.Match.Bind( wx.EVT_BUTTON, self.match )
		self.Unmatch.Bind( wx.EVT_BUTTON, self.unmatch )
		self.m_listCtrl10.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.m_listCtrl10.Bind( wx.EVT_SIZE, self.resize )
		self.m_listCtrl11.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.match )
		self.m_listCtrl11.Bind( wx.EVT_SIZE, self.resize )
		self.m_listCtrl12.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.unmatch )
		self.m_listCtrl12.Bind( wx.EVT_SIZE, self.resize )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def load( self, event ):
		event.Skip()
	
	def save( self, event ):
		event.Skip()
	
	def match( self, event ):
		event.Skip()
	
	def unmatch( self, event ):
		event.Skip()
	
	
	def resize( self, event ):
		event.Skip()
	
	
	
	
	

