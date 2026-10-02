try:
    import wx
except ImportError:
    raise SystemExit(
        "Falta el modulo 'wx' (wxPython).\n"
        "Instalalo con:  py -m pip install wxpython\n"
        "Luego ejecuta este archivo de nuevo."
    )
import math

class CalculadoraWxPython(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None, 
            title="Pract - Calculadora (wxPython)", 
            size=(380, 560),
            style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )
        
        self.historial = []
        self.en_estado_error = False

        self.iniciar_ui()
        self.Centre()

    def iniciar_ui(self):
        # Panel principal
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(30, 30, 30))

        layout_principal = wx.BoxSizer(wx.VERTICAL)

        # 1. Pantalla de Entrada / Resultado
        self.display = wx.TextCtrl(
            panel, 
            style=wx.TE_RIGHT | wx.TE_READONLY | wx.BORDER_NONE
        )
        self.display.SetBackgroundColour(wx.Colour(45, 45, 45))
        self.display.SetForegroundColour(wx.Colour(255, 255, 255))
        self.display.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout_principal.Add(self.display, flag=wx.EXPAND | wx.ALL, border=10)

        # 2. Etiqueta de Historial
        lbl_historial = wx.StaticText(panel, label="Historial (Doble clic para cargar resultado):")
        lbl_historial.SetForegroundColour(wx.Colour(200, 200, 200))
        lbl_historial.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        layout_principal.Add(lbl_historial, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # 3. Lista de Historial Interactivo (wx.ListBox)
        self.list_historial = wx.ListBox(panel, style=wx.LB_SINGLE | wx.BORDER_SIMPLE)
        self.list_historial.SetBackgroundColour(wx.Colour(20, 20, 20))
        self.list_historial.SetForegroundColour(wx.Colour(0, 255, 200))
        self.list_historial.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.list_historial.Bind(wx.EVT_LISTBOX_DCLICK, self.cargar_desde_historial)
        layout_principal.Add(self.list_historial, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # 4. Grid de Botones
        grid_botones = wx.GridSizer(rows=5, cols=4, vgap=5, hgap=5)

        botones = [
            ('C', wx.Colour(180, 50, 50)),   ('CE', wx.Colour(200, 120, 40)), ('/', wx.Colour(60, 80, 100)),  ('*', wx.Colour(60, 80, 100)),
            ('7', wx.Colour(50, 50, 50)),    ('8', wx.Colour(50, 50, 50)),    ('9', wx.Colour(50, 50, 50)),   ('-', wx.Colour(60, 80, 100)),
            ('4', wx.Colour(50, 50, 50)),    ('5', wx.Colour(50, 50, 50)),    ('6', wx.Colour(50, 50, 50)),   ('+', wx.Colour(60, 80, 100)),
            ('1', wx.Colour(50, 50, 50)),    ('2', wx.Colour(50, 50, 50)),    ('3', wx.Colour(50, 50, 50)),   ('=', wx.Colour(0, 120, 215)),
            ('0', wx.Colour(50, 50, 50)),    ('.', wx.Colour(50, 50, 50)),    ('Info', wx.Colour(100, 50, 120))
        ]

        for texto, color in botones:
            btn = wx.Button(panel, label=texto)
            btn.SetBackgroundColour(color)
            btn.SetForegroundColour(wx.Colour(255, 255, 255))
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            
            # Asignar evento al botón
            btn.Bind(wx.EVT_BUTTON, lambda evt, t=texto: self.on_button_click(t))
            grid_botones.Add(btn, 1, wx.EXPAND)

        layout_principal.Add(grid_botones, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(layout_principal)

    def on_button_click(self, texto):
        if texto == 'C':
            self.limpiar()
        elif self.en_estado_error:
            # Si está en error, no permite escribir nada hasta presionar 'C'
            return
        elif texto == 'CE':
            self.borrar_ultimo()
        elif texto == '=':
            self.calcular()
        elif texto == 'Info':
            self.abrir_info()
        else:
            self.agregar_caracter(texto)

    def agregar_caracter(self, char):
        valor_actual = self.display.GetValue()
        self.display.SetValue(valor_actual + char)

    def limpiar(self):
        self.display.SetValue("")
        self.en_estado_error = False

    def borrar_ultimo(self):
        valor_actual = self.display.GetValue()
        if valor_actual:
            self.display.SetValue(valor_actual[:-1])

    def calcular(self):
        expr = self.display.GetValue()
        if not expr:
            return

        try:
            res = eval(expr, {"__builtins__": None, "math": math}, {})
            if isinstance(res, float) and res.is_integer():
                res = int(res)

            res_str = str(res)
            self.actualizar_historial(f"{expr} = {res_str}")
            self.display.SetValue(res_str)
        except Exception:
            self.display.SetValue("Error")
            self.en_estado_error = True

    def actualizar_historial(self, operacion):
        self.historial.append(operacion)
        if len(self.historial) > 5:
            self.historial.pop(0)

        self.list_historial.Clear()
        self.list_historial.Set(self.historial)

    def cargar_desde_historial(self, event):
        # Al hacer doble clic en un ítem del historial, extrae el resultado y lo pone en la pantalla
        seleccion = self.list_historial.GetStringSelection()
        if seleccion and "=" in seleccion:
            resultado = seleccion.split("=")[-1].strip()
            self.display.SetValue(resultado)
            self.en_estado_error = False

    def abrir_info(self):
        wx.MessageBox(
            "Calculadora v4.0\nAutor: Brisa Maribel V.\nLibrería: wxPython",
            "Información",
            wx.OK | wx.ICON_INFORMATION
        )


if __name__ == "__main__":
    app = wx.App()
    frame = CalculadoraWxPython()
    frame.Show()
    app.MainLoop()