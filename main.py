# main.py - Sistema de Gestão de Loja (SisLoja) com interface gráfica
# Ger_estoque = Thiago e Breno
# Ger_cliente = Luan e Vitor
# Ger_caixa = Pedro e Fabiano

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Importar módulos
import estoque_gui
import clientes_gui
import caixa_gui

class SisLojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Loja - SisLoja")
        self.root.geometry("900x650")
        
        # Inicializar módulos ANTES de criar as abas
        self.estoque_module = estoque_gui.EstoqueModule()
        self.clientes_module = clientes_gui.ClientesModule()
        self.caixa_module = caixa_gui.CaixaModule()
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_home_tab()
        self.create_estoque_tab()
        self.create_clientes_tab()
        self.create_caixa_tab()
        self.create_relatorios_tab()
        
        # Barra de status
        self.create_status_bar()
        
    def setup_styles(self):
        """Configura estilos para a interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_home_tab(self):
        """Cria a aba inicial/home"""
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text='🏠 Início')
        
        # Título
        title_label = ttk.Label(home_frame, 
                               text="Sistema de Gestão de Loja (SisLoja)",
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=30)
        
        # Informações do sistema
        info_frame = ttk.LabelFrame(home_frame, text="Informações do Sistema", padding=20)
        info_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        info_text = """Bem-vindo ao SisLoja - Sistema de Gestão de Loja

Módulos disponíveis:
1. 📦 Gestão de Estoque - Controle de produtos e inventário
2. 👥 Gestão de Clientes - Cadastro e administração de clientes
3. 💰 Gestão de Caixa - Controle de vendas e fluxo de caixa
4. 📊 Relatórios - Análises e estatísticas

Desenvolvido por:
• Estoque: Thiago e Breno
• Clientes: Luan e Vitor
• Caixa: Pedro e Fabiano"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify='left', font=('Arial', 11))
        info_label.pack()
        
    def create_estoque_tab(self):
        """Cria a aba de estoque"""
        estoque_frame = ttk.Frame(self.notebook)
        self.notebook.add(estoque_frame, text='📦 Estoque')
        
        # Usar o módulo de estoque
        self.estoque_module.create_interface(estoque_frame)
        
    def create_clientes_tab(self):
        """Cria a aba de clientes"""
        clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(clientes_frame, text='👥 Clientes')
        
        # Usar o módulo de clientes
        self.clientes_module.create_interface(clientes_frame)
        
    def create_caixa_tab(self):
        """Cria a aba de caixa"""
        caixa_frame = ttk.Frame(self.notebook)
        self.notebook.add(caixa_frame, text='💰 Caixa')
        
        # Usar o módulo de caixa
        self.caixa_module.create_interface(caixa_frame)
        
    def create_relatorios_tab(self):
        """Cria a aba de relatórios"""
        relatorios_frame = ttk.Frame(self.notebook)
        self.notebook.add(relatorios_frame, text='📊 Relatórios')
        
        # Título
        ttk.Label(relatorios_frame, text="Relatórios do Sistema",
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame para botões de relatório
        btn_frame = ttk.Frame(relatorios_frame)
        btn_frame.pack(pady=20)
        
        # Botões de relatório
        ttk.Button(btn_frame, text="Relatório de Estoque",
                  command=self.gerar_relatorio_estoque,
                  width=20).grid(row=0, column=0, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Relatório de Clientes",
                  command=self.gerar_relatorio_clientes,
                  width=20).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Relatório de Vendas",
                  command=self.gerar_relatorio_vendas,
                  width=20).grid(row=1, column=0, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Relatório Completo",
                  command=self.gerar_relatorio_completo,
                  width=20).grid(row=1, column=1, padx=10, pady=5)
        
        # Área de exibição do relatório
        ttk.Label(relatorios_frame, text="Relatório:", font=('Arial', 11, 'bold')).pack(pady=(20,5))
        
        from tkinter import scrolledtext
        self.relatorio_text = scrolledtext.ScrolledText(relatorios_frame,
                                                       width=80, height=20,
                                                       font=('Consolas', 10))
        self.relatorio_text.pack(padx=20, pady=5)
        
        # Botões de ação
        action_frame = ttk.Frame(relatorios_frame)
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="Limpar",
                  command=self.limpar_relatorio).pack(side='left', padx=5)
        
        ttk.Button(action_frame, text="Exportar",
                  command=self.exportar_relatorio).pack(side='left', padx=5)
        
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_bar = ttk.Frame(self.root, relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
        
        self.status_label = ttk.Label(self.status_bar, text="Sistema pronto")
        self.status_label.pack(side='left', padx=10)
        
        # Data e hora
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side='right', padx=10)
        
        self.update_time()
        
    def update_time(self):
        """Atualiza a hora na barra de status"""
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)
        
    def gerar_relatorio_estoque(self):
        """Gera relatório de estoque"""
        relatorio = self.estoque_module.gerar_relatorio()
        self.mostrar_relatorio(relatorio, "Estoque")
        
    def gerar_relatorio_clientes(self):
        """Gera relatório de clientes"""
        relatorio = self.clientes_module.gerar_relatorio()
        self.mostrar_relatorio(relatorio, "Clientes")
        
    def gerar_relatorio_vendas(self):
        """Gera relatório de vendas"""
        relatorio = self.caixa_module.gerar_relatorio()
        self.mostrar_relatorio(relatorio, "Vendas")
        
    def gerar_relatorio_completo(self):
        """Gera relatório completo do sistema"""
        relatorio = "=" * 60 + "\n"
        relatorio += "RELATÓRIO COMPLETO DO SISTEMA\n"
        relatorio += "=" * 60 + "\n\n"
        
        relatorio += "1. ESTOQUE:\n" + "=" * 30 + "\n"
        relatorio += self.estoque_module.gerar_relatorio() + "\n\n"
        
        relatorio += "2. CLIENTES:\n" + "=" * 30 + "\n"
        relatorio += self.clientes_module.gerar_relatorio() + "\n\n"
        
        relatorio += "3. VENDAS:\n" + "=" * 30 + "\n"
        relatorio += self.caixa_module.gerar_relatorio() + "\n\n"
        
        relatorio += "Gerado em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        self.mostrar_relatorio(relatorio, "Completo")
        
    def mostrar_relatorio(self, relatorio, tipo):
        """Mostra relatório na área de texto"""
        self.relatorio_text.delete(1.0, tk.END)
        self.relatorio_text.insert(1.0, relatorio)
        self.status_label.config(text=f"Relatório de {tipo} gerado")
        
    def limpar_relatorio(self):
        """Limpa a área de relatório"""
        self.relatorio_text.delete(1.0, tk.END)
        self.status_label.config(text="Relatório limpo")
        
    def exportar_relatorio(self):
        """Exporta o relatório para arquivo"""
        from tkinter import filedialog
        import os
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.relatorio_text.get(1.0, tk.END))
                messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{file_path}")
                self.status_label.config(text=f"Relatório exportado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

def main():
    root = tk.Tk()
    app = SisLojaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()