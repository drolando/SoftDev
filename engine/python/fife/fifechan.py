# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.10
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_fifechan', [dirname(__file__)])
        except ImportError:
            import _fifechan
            return _fifechan
        if fp is not None:
            try:
                _mod = imp.load_module('_fifechan', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _fifechan = swig_import_helper()
    del swig_import_helper
else:
    import _fifechan
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


try:
    import weakref
    weakref_proxy = weakref.proxy
except:
    weakref_proxy = lambda x: x


class MouseListener(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MouseListener, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MouseListener, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _fifechan.delete_MouseListener
    __del__ = lambda self : None;
    def mouseEntered(self, *args): return _fifechan.MouseListener_mouseEntered(self, *args)
    def mouseExited(self, *args): return _fifechan.MouseListener_mouseExited(self, *args)
    def mousePressed(self, *args): return _fifechan.MouseListener_mousePressed(self, *args)
    def mouseReleased(self, *args): return _fifechan.MouseListener_mouseReleased(self, *args)
    def mouseClicked(self, *args): return _fifechan.MouseListener_mouseClicked(self, *args)
    def mouseWheelMovedUp(self, *args): return _fifechan.MouseListener_mouseWheelMovedUp(self, *args)
    def mouseWheelMovedDown(self, *args): return _fifechan.MouseListener_mouseWheelMovedDown(self, *args)
    def mouseMoved(self, *args): return _fifechan.MouseListener_mouseMoved(self, *args)
    def mouseDragged(self, *args): return _fifechan.MouseListener_mouseDragged(self, *args)
    def __init__(self): 
        if self.__class__ == MouseListener:
            _self = None
        else:
            _self = self
        this = _fifechan.new_MouseListener(_self, )
        try: self.this.append(this)
        except: self.this = this
    def __disown__(self):
        self.this.disown()
        _fifechan.disown_MouseListener(self)
        return weakref_proxy(self)
MouseListener_swigregister = _fifechan.MouseListener_swigregister
MouseListener_swigregister(MouseListener)

class KeyListener(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KeyListener, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KeyListener, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _fifechan.delete_KeyListener
    __del__ = lambda self : None;
    def keyPressed(self, *args): return _fifechan.KeyListener_keyPressed(self, *args)
    def keyReleased(self, *args): return _fifechan.KeyListener_keyReleased(self, *args)
    def __init__(self): 
        if self.__class__ == KeyListener:
            _self = None
        else:
            _self = self
        this = _fifechan.new_KeyListener(_self, )
        try: self.this.append(this)
        except: self.this = this
    def __disown__(self):
        self.this.disown()
        _fifechan.disown_KeyListener(self)
        return weakref_proxy(self)
KeyListener_swigregister = _fifechan.KeyListener_swigregister
KeyListener_swigregister(KeyListener)

class ActionListener(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ActionListener, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ActionListener, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _fifechan.delete_ActionListener
    __del__ = lambda self : None;
    def action(self, *args): return _fifechan.ActionListener_action(self, *args)
    def __init__(self): 
        if self.__class__ == ActionListener:
            _self = None
        else:
            _self = self
        this = _fifechan.new_ActionListener(_self, )
        try: self.this.append(this)
        except: self.this = this
    def __disown__(self):
        self.this.disown()
        _fifechan.disown_ActionListener(self)
        return weakref_proxy(self)
ActionListener_swigregister = _fifechan.ActionListener_swigregister
ActionListener_swigregister(ActionListener)

class WidgetListener(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, WidgetListener, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, WidgetListener, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _fifechan.delete_WidgetListener
    __del__ = lambda self : None;
    def widgetResized(self, *args): return _fifechan.WidgetListener_widgetResized(self, *args)
    def widgetMoved(self, *args): return _fifechan.WidgetListener_widgetMoved(self, *args)
    def widgetHidden(self, *args): return _fifechan.WidgetListener_widgetHidden(self, *args)
    def widgetShown(self, *args): return _fifechan.WidgetListener_widgetShown(self, *args)
    def ancestorMoved(self, *args): return _fifechan.WidgetListener_ancestorMoved(self, *args)
    def ancestorHidden(self, *args): return _fifechan.WidgetListener_ancestorHidden(self, *args)
    def ancestorShown(self, *args): return _fifechan.WidgetListener_ancestorShown(self, *args)
    def __init__(self): 
        if self.__class__ == WidgetListener:
            _self = None
        else:
            _self = self
        this = _fifechan.new_WidgetListener(_self, )
        try: self.this.append(this)
        except: self.this = this
    def __disown__(self):
        self.this.disown()
        _fifechan.disown_WidgetListener(self)
        return weakref_proxy(self)
WidgetListener_swigregister = _fifechan.WidgetListener_swigregister
WidgetListener_swigregister(WidgetListener)

class Graphics(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Graphics, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Graphics, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    Left = _fifechan.Graphics_Left
    Center = _fifechan.Graphics_Center
    Right = _fifechan.Graphics_Right
    __swig_destroy__ = _fifechan.delete_Graphics
    __del__ = lambda self : None;
Graphics_swigregister = _fifechan.Graphics_swigregister
Graphics_swigregister(Graphics)

class Color(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Color, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Color, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_Color(*args)
        try: self.this.append(this)
        except: self.this = this
    def __add__(self, *args): return _fifechan.Color___add__(self, *args)
    def __sub__(self, *args): return _fifechan.Color___sub__(self, *args)
    def __mul__(self, *args): return _fifechan.Color___mul__(self, *args)
    def __eq__(self, *args): return _fifechan.Color___eq__(self, *args)
    def __ne__(self, *args): return _fifechan.Color___ne__(self, *args)
    __swig_setmethods__["r"] = _fifechan.Color_r_set
    __swig_getmethods__["r"] = _fifechan.Color_r_get
    if _newclass:r = _swig_property(_fifechan.Color_r_get, _fifechan.Color_r_set)
    __swig_setmethods__["g"] = _fifechan.Color_g_set
    __swig_getmethods__["g"] = _fifechan.Color_g_get
    if _newclass:g = _swig_property(_fifechan.Color_g_get, _fifechan.Color_g_set)
    __swig_setmethods__["b"] = _fifechan.Color_b_set
    __swig_getmethods__["b"] = _fifechan.Color_b_get
    if _newclass:b = _swig_property(_fifechan.Color_b_get, _fifechan.Color_b_set)
    __swig_setmethods__["a"] = _fifechan.Color_a_set
    __swig_getmethods__["a"] = _fifechan.Color_a_get
    if _newclass:a = _swig_property(_fifechan.Color_a_get, _fifechan.Color_a_set)
    __swig_destroy__ = _fifechan.delete_Color
    __del__ = lambda self : None;
Color_swigregister = _fifechan.Color_swigregister
Color_swigregister(Color)

class Widget(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Widget, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Widget, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    def setWidth(self, *args): return _fifechan.Widget_setWidth(self, *args)
    def getWidth(self): return _fifechan.Widget_getWidth(self)
    def setHeight(self, *args): return _fifechan.Widget_setHeight(self, *args)
    def getHeight(self): return _fifechan.Widget_getHeight(self)
    def setSize(self, *args): return _fifechan.Widget_setSize(self, *args)
    def setX(self, *args): return _fifechan.Widget_setX(self, *args)
    def getX(self): return _fifechan.Widget_getX(self)
    def setY(self, *args): return _fifechan.Widget_setY(self, *args)
    def getY(self): return _fifechan.Widget_getY(self)
    def setPosition(self, *args): return _fifechan.Widget_setPosition(self, *args)
    def setFrameSize(self, *args): return _fifechan.Widget_setFrameSize(self, *args)
    def getFrameSize(self): return _fifechan.Widget_getFrameSize(self)
    def setFocusable(self, *args): return _fifechan.Widget_setFocusable(self, *args)
    def isFocusable(self): return _fifechan.Widget_isFocusable(self)
    def isFocused(self): return _fifechan.Widget_isFocused(self)
    def setEnabled(self, *args): return _fifechan.Widget_setEnabled(self, *args)
    def isEnabled(self): return _fifechan.Widget_isEnabled(self)
    def setVisible(self, *args): return _fifechan.Widget_setVisible(self, *args)
    def isVisible(self): return _fifechan.Widget_isVisible(self)
    def setBaseColor(self, *args): return _fifechan.Widget_setBaseColor(self, *args)
    def getBaseColor(self): return _fifechan.Widget_getBaseColor(self)
    def setForegroundColor(self, *args): return _fifechan.Widget_setForegroundColor(self, *args)
    def getForegroundColor(self): return _fifechan.Widget_getForegroundColor(self)
    def setBackgroundColor(self, *args): return _fifechan.Widget_setBackgroundColor(self, *args)
    def getBackgroundColor(self): return _fifechan.Widget_getBackgroundColor(self)
    def setSelectionColor(self, *args): return _fifechan.Widget_setSelectionColor(self, *args)
    def getSelectionColor(self): return _fifechan.Widget_getSelectionColor(self)
    def requestFocus(self): return _fifechan.Widget_requestFocus(self)
    def requestMoveToTop(self): return _fifechan.Widget_requestMoveToTop(self)
    def requestMoveToBottom(self): return _fifechan.Widget_requestMoveToBottom(self)
    def setActionEventId(self, *args): return _fifechan.Widget_setActionEventId(self, *args)
    def getActionEventId(self): return _fifechan.Widget_getActionEventId(self)
    def getAbsolutePosition(self, *args): return _fifechan.Widget_getAbsolutePosition(self, *args)
    def getFont(self): return _fifechan.Widget_getFont(self)
    __swig_getmethods__["setGlobalFont"] = lambda x: _fifechan.Widget_setGlobalFont
    if _newclass:setGlobalFont = staticmethod(_fifechan.Widget_setGlobalFont)
    def setFont(self, *args): return _fifechan.Widget_setFont(self, *args)
    def isTabInEnabled(self): return _fifechan.Widget_isTabInEnabled(self)
    def setTabInEnabled(self, *args): return _fifechan.Widget_setTabInEnabled(self, *args)
    def isTabOutEnabled(self): return _fifechan.Widget_isTabOutEnabled(self)
    def setTabOutEnabled(self, *args): return _fifechan.Widget_setTabOutEnabled(self, *args)
    def requestModalFocus(self): return _fifechan.Widget_requestModalFocus(self)
    def requestModalMouseInputFocus(self): return _fifechan.Widget_requestModalMouseInputFocus(self)
    def releaseModalFocus(self): return _fifechan.Widget_releaseModalFocus(self)
    def releaseModalMouseInputFocus(self): return _fifechan.Widget_releaseModalMouseInputFocus(self)
    def isModalFocused(self): return _fifechan.Widget_isModalFocused(self)
    def isModalMouseInputFocused(self): return _fifechan.Widget_isModalMouseInputFocused(self)
    def getWidgetAt(self, *args): return _fifechan.Widget_getWidgetAt(self, *args)
    def moveToTop(self, *args): return _fifechan.Widget_moveToTop(self, *args)
    def moveToBottom(self, *args): return _fifechan.Widget_moveToBottom(self, *args)
    def focusNext(self): return _fifechan.Widget_focusNext(self)
    def focusPrevious(self): return _fifechan.Widget_focusPrevious(self)
    def addActionListener(self, *args): return _fifechan.Widget_addActionListener(self, *args)
    def removeActionListener(self, *args): return _fifechan.Widget_removeActionListener(self, *args)
    def addMouseListener(self, *args): return _fifechan.Widget_addMouseListener(self, *args)
    def removeMouseListener(self, *args): return _fifechan.Widget_removeMouseListener(self, *args)
    def addKeyListener(self, *args): return _fifechan.Widget_addKeyListener(self, *args)
    def removeKeyListener(self, *args): return _fifechan.Widget_removeKeyListener(self, *args)
    def addWidgetListener(self, *args): return _fifechan.Widget_addWidgetListener(self, *args)
    def removeWidgetListener(self, *args): return _fifechan.Widget_removeWidgetListener(self, *args)
    def draw(self, *args): return _fifechan.Widget_draw(self, *args)
    __swig_destroy__ = _fifechan.delete_Widget
    __del__ = lambda self : None;
Widget_swigregister = _fifechan.Widget_swigregister
Widget_swigregister(Widget)

def Widget_setGlobalFont(*args):
  return _fifechan.Widget_setGlobalFont(*args)
Widget_setGlobalFont = _fifechan.Widget_setGlobalFont

class Container(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Container, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, Container, name)
    __repr__ = _swig_repr
    def __init__(self): 
        this = _fifechan.new_Container()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_Container
    __del__ = lambda self : None;
    def setOpaque(self, *args): return _fifechan.Container_setOpaque(self, *args)
    def isOpaque(self): return _fifechan.Container_isOpaque(self)
    def add(self, *args): return _fifechan.Container_add(self, *args)
    def remove(self, *args): return _fifechan.Container_remove(self, *args)
    def clear(self): return _fifechan.Container_clear(self)
Container_swigregister = _fifechan.Container_swigregister
Container_swigregister(Container)

class CheckBox(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CheckBox, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, CheckBox, name)
    __repr__ = _swig_repr
    def __init__(self): 
        this = _fifechan.new_CheckBox()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_CheckBox
    __del__ = lambda self : None;
    def isSelected(self): return _fifechan.CheckBox_isSelected(self)
    def setSelected(self, *args): return _fifechan.CheckBox_setSelected(self, *args)
    def getCaption(self): return _fifechan.CheckBox_getCaption(self)
    def setCaption(self, *args): return _fifechan.CheckBox_setCaption(self, *args)
    def adjustSize(self): return _fifechan.CheckBox_adjustSize(self)
CheckBox_swigregister = _fifechan.CheckBox_swigregister
CheckBox_swigregister(CheckBox)

class Button(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Button, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, Button, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_Button(*args)
        try: self.this.append(this)
        except: self.this = this
    def setCaption(self, *args): return _fifechan.Button_setCaption(self, *args)
    def getCaption(self): return _fifechan.Button_getCaption(self)
    def setAlignment(self, *args): return _fifechan.Button_setAlignment(self, *args)
    def getAlignment(self): return _fifechan.Button_getAlignment(self)
    def adjustSize(self): return _fifechan.Button_adjustSize(self)
    __swig_destroy__ = _fifechan.delete_Button
    __del__ = lambda self : None;
Button_swigregister = _fifechan.Button_swigregister
Button_swigregister(Button)

class ScrollArea(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ScrollArea, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, ScrollArea, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_ScrollArea(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_ScrollArea
    __del__ = lambda self : None;
    def setContent(self, *args): return _fifechan.ScrollArea_setContent(self, *args)
    def getContent(self): return _fifechan.ScrollArea_getContent(self)
    def setHorizontalScrollPolicy(self, *args): return _fifechan.ScrollArea_setHorizontalScrollPolicy(self, *args)
    def getHorizontalScrollPolicy(self): return _fifechan.ScrollArea_getHorizontalScrollPolicy(self)
    def setVerticalScrollPolicy(self, *args): return _fifechan.ScrollArea_setVerticalScrollPolicy(self, *args)
    def getVerticalScrollPolicy(self): return _fifechan.ScrollArea_getVerticalScrollPolicy(self)
    def setScrollPolicy(self, *args): return _fifechan.ScrollArea_setScrollPolicy(self, *args)
    def setVerticalScrollAmount(self, *args): return _fifechan.ScrollArea_setVerticalScrollAmount(self, *args)
    def getVerticalScrollAmount(self): return _fifechan.ScrollArea_getVerticalScrollAmount(self)
    def setHorizontalScrollAmount(self, *args): return _fifechan.ScrollArea_setHorizontalScrollAmount(self, *args)
    def getHorizontalScrollAmount(self): return _fifechan.ScrollArea_getHorizontalScrollAmount(self)
    def setScrollAmount(self, *args): return _fifechan.ScrollArea_setScrollAmount(self, *args)
    def getHorizontalMaxScroll(self): return _fifechan.ScrollArea_getHorizontalMaxScroll(self)
    def getVerticalMaxScroll(self): return _fifechan.ScrollArea_getVerticalMaxScroll(self)
    def setScrollbarWidth(self, *args): return _fifechan.ScrollArea_setScrollbarWidth(self, *args)
    def getScrollbarWidth(self): return _fifechan.ScrollArea_getScrollbarWidth(self)
    def setLeftButtonScrollAmount(self, *args): return _fifechan.ScrollArea_setLeftButtonScrollAmount(self, *args)
    def setRightButtonScrollAmount(self, *args): return _fifechan.ScrollArea_setRightButtonScrollAmount(self, *args)
    def setUpButtonScrollAmount(self, *args): return _fifechan.ScrollArea_setUpButtonScrollAmount(self, *args)
    def setDownButtonScrollAmount(self, *args): return _fifechan.ScrollArea_setDownButtonScrollAmount(self, *args)
    def getLeftButtonScrollAmount(self): return _fifechan.ScrollArea_getLeftButtonScrollAmount(self)
    def getRightButtonScrollAmount(self): return _fifechan.ScrollArea_getRightButtonScrollAmount(self)
    def getUpButtonScrollAmount(self): return _fifechan.ScrollArea_getUpButtonScrollAmount(self)
    def getDownButtonScrollAmount(self): return _fifechan.ScrollArea_getDownButtonScrollAmount(self)
    ShowAlways = _fifechan.ScrollArea_ShowAlways
    ShowNever = _fifechan.ScrollArea_ShowNever
    ShowAuto = _fifechan.ScrollArea_ShowAuto
ScrollArea_swigregister = _fifechan.ScrollArea_swigregister
ScrollArea_swigregister(ScrollArea)

class ListModel(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ListModel, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ListModel, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _fifechan.delete_ListModel
    __del__ = lambda self : None;
    def getNumberOfElements(self): return _fifechan.ListModel_getNumberOfElements(self)
    def getElementAt(self, *args): return _fifechan.ListModel_getElementAt(self, *args)
    def __init__(self): 
        if self.__class__ == ListModel:
            _self = None
        else:
            _self = self
        this = _fifechan.new_ListModel(_self, )
        try: self.this.append(this)
        except: self.this = this
    def __disown__(self):
        self.this.disown()
        _fifechan.disown_ListModel(self)
        return weakref_proxy(self)
ListModel_swigregister = _fifechan.ListModel_swigregister
ListModel_swigregister(ListModel)

class ListBox(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ListBox, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, ListBox, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_ListBox(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_ListBox
    __del__ = lambda self : None;
    def getSelected(self): return _fifechan.ListBox_getSelected(self)
    def setSelected(self, *args): return _fifechan.ListBox_setSelected(self, *args)
    def setListModel(self, *args): return _fifechan.ListBox_setListModel(self, *args)
    def getListModel(self): return _fifechan.ListBox_getListModel(self)
    def adjustSize(self): return _fifechan.ListBox_adjustSize(self)
    def isWrappingEnabled(self): return _fifechan.ListBox_isWrappingEnabled(self)
    def setWrappingEnabled(self, *args): return _fifechan.ListBox_setWrappingEnabled(self, *args)
ListBox_swigregister = _fifechan.ListBox_swigregister
ListBox_swigregister(ListBox)

class DropDown(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DropDown, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, DropDown, name)
    __repr__ = _swig_repr
    def __init__(self, listModel=None, scrollArea=None, listBox=None): 
        this = _fifechan.new_DropDown(listModel, scrollArea, listBox)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_DropDown
    __del__ = lambda self : None;
    def getSelected(self): return _fifechan.DropDown_getSelected(self)
    def setSelected(self, *args): return _fifechan.DropDown_setSelected(self, *args)
    def setListModel(self, *args): return _fifechan.DropDown_setListModel(self, *args)
    def getListModel(self): return _fifechan.DropDown_getListModel(self)
    def adjustHeight(self): return _fifechan.DropDown_adjustHeight(self)
    def setBaseColor(self, *args): return _fifechan.DropDown_setBaseColor(self, *args)
    def getBaseColor(self): return _fifechan.DropDown_getBaseColor(self)
    def setForegroundColor(self, *args): return _fifechan.DropDown_setForegroundColor(self, *args)
    def getForegroundColor(self): return _fifechan.DropDown_getForegroundColor(self)
    def setBackgroundColor(self, *args): return _fifechan.DropDown_setBackgroundColor(self, *args)
    def getBackgroundColor(self): return _fifechan.DropDown_getBackgroundColor(self)
    def setSelectionColor(self, *args): return _fifechan.DropDown_setSelectionColor(self, *args)
    def getSelectionColor(self): return _fifechan.DropDown_getSelectionColor(self)
DropDown_swigregister = _fifechan.DropDown_swigregister
DropDown_swigregister(DropDown)

class RadioButton(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, RadioButton, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, RadioButton, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_RadioButton(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_RadioButton
    __del__ = lambda self : None;
    def isSelected(self): return _fifechan.RadioButton_isSelected(self)
    def setSelected(self, *args): return _fifechan.RadioButton_setSelected(self, *args)
    def getCaption(self): return _fifechan.RadioButton_getCaption(self)
    def setCaption(self, *args): return _fifechan.RadioButton_setCaption(self, *args)
    def setGroup(self, *args): return _fifechan.RadioButton_setGroup(self, *args)
    def getGroup(self): return _fifechan.RadioButton_getGroup(self)
    def adjustSize(self): return _fifechan.RadioButton_adjustSize(self)
RadioButton_swigregister = _fifechan.RadioButton_swigregister
RadioButton_swigregister(RadioButton)

class Slider(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Slider, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, Slider, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_Slider(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_Slider
    __del__ = lambda self : None;
    def setScale(self, *args): return _fifechan.Slider_setScale(self, *args)
    def getScaleStart(self): return _fifechan.Slider_getScaleStart(self)
    def setScaleStart(self, *args): return _fifechan.Slider_setScaleStart(self, *args)
    def getScaleEnd(self): return _fifechan.Slider_getScaleEnd(self)
    def setScaleEnd(self, *args): return _fifechan.Slider_setScaleEnd(self, *args)
    def getValue(self): return _fifechan.Slider_getValue(self)
    def setValue(self, *args): return _fifechan.Slider_setValue(self, *args)
    def setMarkerLength(self, *args): return _fifechan.Slider_setMarkerLength(self, *args)
    def getMarkerLength(self): return _fifechan.Slider_getMarkerLength(self)
    def setOrientation(self, *args): return _fifechan.Slider_setOrientation(self, *args)
    def getOrientation(self): return _fifechan.Slider_getOrientation(self)
    def setStepLength(self, *args): return _fifechan.Slider_setStepLength(self, *args)
    def getStepLength(self): return _fifechan.Slider_getStepLength(self)
    Horizontal = _fifechan.Slider_Horizontal
    Vertical = _fifechan.Slider_Vertical
Slider_swigregister = _fifechan.Slider_swigregister
Slider_swigregister(Slider)

class Window(Container):
    __swig_setmethods__ = {}
    for _s in [Container]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Window, name, value)
    __swig_getmethods__ = {}
    for _s in [Container]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, Window, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_Window(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_Window
    __del__ = lambda self : None;
    def setCaption(self, *args): return _fifechan.Window_setCaption(self, *args)
    def getCaption(self): return _fifechan.Window_getCaption(self)
    def setAlignment(self, *args): return _fifechan.Window_setAlignment(self, *args)
    def getAlignment(self): return _fifechan.Window_getAlignment(self)
    def setPadding(self, *args): return _fifechan.Window_setPadding(self, *args)
    def getPadding(self): return _fifechan.Window_getPadding(self)
    def setTitleBarHeight(self, *args): return _fifechan.Window_setTitleBarHeight(self, *args)
    def getTitleBarHeight(self): return _fifechan.Window_getTitleBarHeight(self)
    def setMovable(self, *args): return _fifechan.Window_setMovable(self, *args)
    def isMovable(self): return _fifechan.Window_isMovable(self)
    def setOpaque(self, *args): return _fifechan.Window_setOpaque(self, *args)
    def isOpaque(self): return _fifechan.Window_isOpaque(self)
    def resizeToContent(self): return _fifechan.Window_resizeToContent(self)
Window_swigregister = _fifechan.Window_swigregister
Window_swigregister(Window)

class TextBox(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, TextBox, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, TextBox, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_TextBox(*args)
        try: self.this.append(this)
        except: self.this = this
    def setText(self, *args): return _fifechan.TextBox_setText(self, *args)
    def getText(self): return _fifechan.TextBox_getText(self)
    def getTextRow(self, *args): return _fifechan.TextBox_getTextRow(self, *args)
    def setTextRow(self, *args): return _fifechan.TextBox_setTextRow(self, *args)
    def getNumberOfRows(self): return _fifechan.TextBox_getNumberOfRows(self)
    def getCaretPosition(self): return _fifechan.TextBox_getCaretPosition(self)
    def setCaretPosition(self, *args): return _fifechan.TextBox_setCaretPosition(self, *args)
    def getCaretRow(self): return _fifechan.TextBox_getCaretRow(self)
    def setCaretRow(self, *args): return _fifechan.TextBox_setCaretRow(self, *args)
    def getCaretColumn(self): return _fifechan.TextBox_getCaretColumn(self)
    def setCaretColumn(self, *args): return _fifechan.TextBox_setCaretColumn(self, *args)
    def setCaretRowColumn(self, *args): return _fifechan.TextBox_setCaretRowColumn(self, *args)
    def scrollToCaret(self): return _fifechan.TextBox_scrollToCaret(self)
    def isEditable(self): return _fifechan.TextBox_isEditable(self)
    def setEditable(self, *args): return _fifechan.TextBox_setEditable(self, *args)
    def addRow(self, *args): return _fifechan.TextBox_addRow(self, *args)
    def isOpaque(self): return _fifechan.TextBox_isOpaque(self)
    def setOpaque(self, *args): return _fifechan.TextBox_setOpaque(self, *args)
    __swig_destroy__ = _fifechan.delete_TextBox
    __del__ = lambda self : None;
TextBox_swigregister = _fifechan.TextBox_swigregister
TextBox_swigregister(TextBox)

class TextField(Widget):
    __swig_setmethods__ = {}
    for _s in [Widget]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, TextField, name, value)
    __swig_getmethods__ = {}
    for _s in [Widget]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, TextField, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _fifechan.new_TextField(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _fifechan.delete_TextField
    __del__ = lambda self : None;
    def setText(self, *args): return _fifechan.TextField_setText(self, *args)
    def getText(self): return _fifechan.TextField_getText(self)
    def adjustSize(self): return _fifechan.TextField_adjustSize(self)
    def adjustHeight(self): return _fifechan.TextField_adjustHeight(self)
    def setCaretPosition(self, *args): return _fifechan.TextField_setCaretPosition(self, *args)
    def getCaretPosition(self): return _fifechan.TextField_getCaretPosition(self)
TextField_swigregister = _fifechan.TextField_swigregister
TextField_swigregister(TextField)

# This file is compatible with both classic and new-style classes.


