# caixa_gui.py - Módulo de gestão de caixa

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class CaixaModule:
    def __init__(self):
        self.vendas_file = "vendas.json"
        self.vendas = []
        self.carregar_vendas()
        
    def carregar_vendas(self):
        """Carrega vendas do arquivo JSON"""
        if os.path.exists(self.vendas_file):
            try:
                with open(self.vendas_file, 'r', encoding='utf-8') as f:
                    self.vendas = json.load(f)
            except:
                self.vendas = []
        else:
            self.vendas = []
            
    def salvar_vendas(self):
        """Salva vendas no arquivo JSON"""
        try:
            with open(self.vendas_file, 'w', encoding='utf-8') as f:
                json.dump(self.vendas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar vendas: {str(e)}")
            
    def create_interface(self, parent):
        """Cria a interface do módulo de caixa"""
        self.itens_venda = []  # Inicializar lista de itens da venda atual
        
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de nova venda (esquerda)
        venda_frame = ttk.LabelFrame(main_frame, text="Nova Venda", padding=10)
        venda_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Campos da venda
        ttk.Label(venda_frame, text="Data (DD/MM/AAAA):").grid(row=0, column=0, sticky='w', pady=5)
        self.data_entry = ttk.Entry(venda_frame, width=20)
        self.data_entry.grid(row=0, column=1, pady=5, padx=5)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(venda_frame, text="CPF do Cliente:").grid(row=1, column=0, sticky='w', pady=5)
        self.cpf_venda_entry = ttk.Entry(venda_frame, width=20)
        self.cpf_venda_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Frame para itens da venda
        ttk.Label(venda_frame, text="Adicionar Item:", font=('Arial', 10, 'bold')).grid(row=2, column=0, columnspan=2, pady=10, sticky='w')
        
        add_frame = ttk.Frame(venda_frame)
        add_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky='ew')
        
        ttk.Label(add_frame, text="Código:").pack(side='left', padx=2)
        self.codigo_item_entry = ttk.Entry(add_frame, width=10)
        self.codigo_item_entry.pack(side='left', padx=2)
        
        ttk.Label(add_frame, text="Qtd:").pack(side='left', padx=2)
        self.qtd_item_entry = ttk.Entry(add_frame, width=5)
        self.qtd_item_entry.pack(side='left', padx=2)
        
        ttk.Label(add_frame, text="Valor R$:").pack(side='left', padx=2)
        self.valor_item_entry = ttk.Entry(add_frame, width=10)
        self.valor_item_entry.pack(side='left', padx=2)
        
        ttk.Button(add_frame, text="+ Adicionar",
                  command=self.adicionar_item_venda,
                  width=12).pack(side='left', padx=5)
        
        # Lista de itens da venda atual
        ttk.Label(venda_frame, text="Itens da Venda:", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, pady=(10,5), sticky='w')
        
        itens_frame = ttk.Frame(venda_frame)
        itens_frame.grid(row=5, column=0, columnspan=2, pady=5, sticky='nsew')
        
        # Treeview para itens
        columns = ('Código', 'Qtd', 'Valor Unit.', 'Subtotal')
        self.itens_tree = ttk.Treeview(itens_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.itens_tree.heading(col, text=col)
            self.itens_tree.column(col, width=70)
            
        self.itens_tree.pack()
        
        # Total da venda
        ttk.Label(venda_frame, text="Total da Venda:", 
                 font=('Arial', 11, 'bold')).grid(row=6, column=0, sticky='w', pady=10)
        self.total_venda_label = ttk.Label(venda_frame, text="R$ 0,00", 
                                          font=('Arial', 12, 'bold'), foreground='green')
        self.total_venda_label.grid(row=6, column=1, pady=10, sticky='w')
        
        # Botões da venda
        btn_frame = ttk.Frame(venda_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Finalizar Venda",
                  command=self.finalizar_venda,
                  width=15).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar Venda",
                  command=self.cancelar_venda,
                  width=15).pack(side='left', padx=5)
        
        # Frame do histórico (direita)
        historico_frame = ttk.LabelFrame(main_frame, text="Histórico de Vendas", padding=10)
        historico_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview para histórico
        columns = ('Data', 'CPF', 'Itens', 'Total')
        self.historico_tree = ttk.Treeview(historico_frame, columns=columns, show='headings', height=15)
        
        col_configs = [
            ('Data', 80),
            ('CPF', 100),
            ('Itens', 100),
            ('Total', 100)
        ]
        
        for col, width in col_configs:
            self.historico_tree.heading(col, text=col)
            self.historico_tree.column(col, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(historico_frame, orient='vertical', command=self.historico_tree.yview)
        self.historico_tree.configure(yscrollcommand=scrollbar.set)
        
        self.historico_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botão para atualizar histórico
        ttk.Button(historico_frame, text="Atualizar Histórico",
                  command=self.atualizar_historico).pack(pady=5)
        
        # Inicializar
        self.atualizar_historico()
        
    def adicionar_item_venda(self):
        """Adiciona item à venda atual"""
        try:
            codigo = self.codigo_item_entry.get().strip()
            quantidade = int(self.qtd_item_entry.get()) if self.qtd_item_entry.get() else 0
            valor = float(self.valor_item_entry.get().replace(',', '.')) if self.valor_item_entry.get() else 0
            
            if not codigo or quantidade <= 0 or valor <= 0:
                messagebox.showerror("Erro", "Valores inválidos para o item!")
                return
                
            subtotal = quantidade * valor
            
            # Adicionar à lista
            item = {
                'codigo': codigo,
                'quantidade': quantidade,
                'valor': valor,
                'subtotal': subtotal
            }
            self.itens_venda.append(item)
            
            # Adicionar à treeview
            self.itens_tree.insert('', 'end', values=(
                codigo,
                quantidade,
                f"R$ {valor:.2f}",
                f"R$ {subtotal:.2f}"
            ))
            
            # Atualizar total
            self.atualizar_total_venda()
            
            # Limpar campos
            self.codigo_item_entry.delete(0, tk.END)
            self.qtd_item_entry.delete(0, tk.END)
            self.valor_item_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos! Use números.")
            
    def atualizar_total_venda(self):
        """Atualiza o total da venda atual"""
        total = sum(item['subtotal'] for item in self.itens_venda)
        self.total_venda_label.config(text=f"R$ {total:.2f}")
        
    def finalizar_venda(self):
        """Finaliza a venda atual"""
        if not self.itens_venda:
            messagebox.showerror("Erro", "Adicione itens à venda!")
            return
            
        try:
            data = self.data_entry.get().strip()
            cpf = self.cpf_venda_entry.get().strip()
            total = sum(item['subtotal'] for item in self.itens_venda)
            
            if not data or not cpf:
                messagebox.showerror("Erro", "Data e CPF são obrigatórios!")
                return
            
            # Criar registro da venda
            nova_venda = {
                'id': len(self.vendas) + 1,
                'data': data,
                'cpf': cpf,
                'itens': self.itens_venda.copy(),
                'total': total,
                'data_registro': datetime.now().isoformat()
            }
            
            self.vendas.append(nova_venda)
            self.salvar_vendas()
            
            messagebox.showinfo("Sucesso", f"Venda #{nova_venda['id']} finalizada!\nTotal: R$ {total:.2f}")
            
            # Limpar venda atual
            self.cancelar_venda()
            self.atualizar_historico()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
            
    def cancelar_venda(self):
        """Cancela a venda atual"""
        self.itens_venda = []
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        self.total_venda_label.config(text="R$ 0,00")
        self.cpf_venda_entry.delete(0, tk.END)
        
    def atualizar_historico(self):
        """Atualiza o histórico de vendas"""
        # Limpar histórico atual
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
            
        # Adicionar vendas (últimas 20)
        for venda in self.vendas[-20:]:
            num_itens = len(venda['itens'])
            self.historico_tree.insert('', 'end', values=(
                venda['data'],
                venda['cpf'],
                f"{num_itens} itens",
                f"R$ {venda['total']:.2f}"
            ))
            
    def gerar_relatorio(self):
        """Gera relatório de vendas"""
        if not self.vendas:
            return "Nenhuma venda registrada.\n\nRegistre vendas para gerar relatórios."
            
        relatorio = "=" * 50 + "\n"
        relatorio += "RELATÓRIO DE VENDAS\n"
        relatorio += "=" * 50 + "\n\n"
        
        total_vendas = len(self.vendas)
        valor_total = sum(v['total'] for v in self.vendas)
        media_venda = valor_total / total_vendas if total_vendas > 0 else 0
        
        # Vendas por período
        hoje = datetime.now()
        vendas_hoje = [
            v for v in self.vendas 
            if datetime.fromisoformat(v['data_registro']).date() == hoje.date()
        ]
        
        relatorio += f"RESUMO:\n"
        relatorio += f"- Total de vendas: {total_vendas}\n"
        relatorio += f"- Valor total vendido: R$ {valor_total:.2f}\n"
        relatorio += f"- Valor médio por venda: R$ {media_venda:.2f}\n"
        relatorio += f"- Vendas hoje: {len(vendas_hoje)}\n\n"
        
        relatorio += "ÚLTIMAS VENDAS:\n"
        relatorio += "-" * 70 + "\n"
        
        # Últimas 10 vendas
        for venda in self.vendas[-10:]:
            relatorio += f"Venda #{venda['id']:04d} | "
            relatorio += f"Data: {venda['data']} | "
            relatorio += f"CPF: {venda['cpf']} | "
            relatorio += f"Itens: {len(venda['itens']):2d} | "
            relatorio += f"Total: R$ {venda['total']:>8.2f}\n"
            
        relatorio += "-" * 70 + "\n"
        
        # Itens mais vendidos
        if self.vendas:
            relatorio += "\nITENS MAIS VENDIDOS:\n"
            from collections import Counter
            todos_itens = []
            for venda in self.vendas:
                for item in venda['itens']:
                    todos_itens.append(item['codigo'])
            
            if todos_itens:
                contador = Counter(todos_itens)
                for codigo, quantidade in contador.most_common(5):
                    relatorio += f"- Código {codigo}: {quantidade} vendas\n"
        
        relatorio += f"\nGerado em: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        return relatorio