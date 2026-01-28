# estoque_gui.py - Módulo de gestão de estoque

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class EstoqueModule:
    def __init__(self):
        self.estoque_file = "estoque.json"
        self.estoque = []
        self.carregar_estoque()
        
    def carregar_estoque(self):
        """Carrega o estoque do arquivo JSON"""
        if os.path.exists(self.estoque_file):
            try:
                with open(self.estoque_file, 'r', encoding='utf-8') as f:
                    self.estoque = json.load(f)
            except:
                self.estoque = []
        else:
            self.estoque = []
            
    def salvar_estoque(self):
        """Salva o estoque no arquivo JSON"""
        try:
            with open(self.estoque_file, 'w', encoding='utf-8') as f:
                json.dump(self.estoque, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar estoque: {str(e)}")
            
    def create_interface(self, parent):
        """Cria a interface do módulo de estoque"""
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de controle (esquerda)
        control_frame = ttk.LabelFrame(main_frame, text="Controle de Estoque", padding=10)
        control_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Campos de entrada
        campos = [
            ("Código:", "codigo_entry"),
            ("Nome:", "nome_entry"),
            ("Descrição:", "descricao_entry"),
            ("Valor Unitário R$:", "valor_entry"),
            ("Quantidade:", "quantidade_entry")
        ]
        
        for i, (label, var_name) in enumerate(campos):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(control_frame, width=25)
            entry.grid(row=i, column=1, pady=5, padx=5)
            setattr(self, var_name, entry)
            
        # Botões de ação
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Adicionar", 
                  command=self.adicionar_item,
                  width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remover",
                  command=self.remover_item,
                  width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Atualizar",
                  command=self.atualizar_item,
                  width=12).pack(side='left', padx=2)
        
        ttk.Button(control_frame, text="Limpar Campos",
                  command=self.limpar_campos,
                  width=25).grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
        
        # Frame da lista (direita)
        list_frame = ttk.LabelFrame(main_frame, text="Itens em Estoque", padding=10)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview para mostrar estoque
        columns = ('Código', 'Nome', 'Valor', 'Quantidade', 'Total')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        col_configs = [
            ('Código', 80),
            ('Nome', 150),
            ('Valor', 80),
            ('Quantidade', 80),
            ('Total', 100)
        ]
        
        for col, width in col_configs:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botão para carregar dados
        ttk.Button(list_frame, text="Atualizar Lista",
                  command=self.atualizar_lista).pack(pady=5)
        
        # Bind para seleção na treeview
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        
        # Inicializar lista
        self.atualizar_lista()
        
    def adicionar_item(self):
        """Adiciona um novo item ao estoque"""
        try:
            codigo = int(self.codigo_entry.get().strip())
            nome = str(self.nome_entry.get().strip())
            descricao = self.descricao_entry.get().strip()
            valor = float(self.valor_entry.get().replace(',', '.')) if self.valor_entry.get() else 0
            quantidade = int(self.quantidade_entry.get()) if self.quantidade_entry.get() else 0
            
            if not codigo or not nome:
                messagebox.showerror("Erro", "Código e nome são obrigatórios!")
                return

            if not isinstance(codigo, int):
                messagebox.showerror("Erro", "Código deve ser um número inteiro!")
                return
            if quantidade < 0 or valor < 0:
                messagebox.showerror("Erro", "Valor e quantidade não podem ser negativos!")
                return
            # Verificar se código já existe
            for item in self.estoque:
                if item['codigo'] == codigo:
                    resposta = messagebox.askyesno("Item existente", 
                                                  "Código já existe! Deseja atualizar a quantidade?")
                    if resposta:
                        item['quantidade'] += quantidade
                        item['total'] = item['valor'] * item['quantidade']
                        self.salvar_estoque()
                        self.atualizar_lista()
                        self.limpar_campos()
                        messagebox.showinfo("Sucesso", "Quantidade atualizada!")
                    return
            
            # Adicionar item
            novo_item = {
                'codigo': codigo,
                'nome': nome,
                'descricao': descricao,
                'valor': valor,
                'quantidade': quantidade,
                'total': valor * quantidade
            }
            
            self.estoque.append(novo_item)
            self.salvar_estoque()
            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Item adicionado com sucesso!")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Valores inválidos!\n{str(e)}")
            
    def remover_item(self):
        """Remove o item selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return
            
        item = self.tree.item(selecionado[0])
        codigo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Remover item '{codigo}'?"):
            self.estoque = [item for item in self.estoque if item['codigo'] != codigo]
            self.salvar_estoque()
            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
            
    def atualizar_item(self):
        """Atualiza o item selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para atualizar!")
            return
            
        try:
            codigo = self.codigo_entry.get().strip()
            nome = self.nome_entry.get().strip()
            descricao = self.descricao_entry.get().strip()
            valor = float(self.valor_entry.get().replace(',', '.')) if self.valor_entry.get() else 0
            quantidade = int(self.quantidade_entry.get()) if self.quantidade_entry.get() else 0
            
            # Atualizar item
            for item in self.estoque:
                if item['codigo'] == codigo:
                    item.update({
                        'nome': nome,
                        'descricao': descricao,
                        'valor': valor,
                        'quantidade': quantidade,
                        'total': valor * quantidade
                    })
                    break
            
            self.salvar_estoque()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
            
    def item_selecionado(self, event):
        """Preenche os campos quando um item é selecionado"""
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado[0])
            valores = item['values']
            
            self.codigo_entry.delete(0, tk.END)
            self.codigo_entry.insert(0, valores[0])
            
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, valores[1])
            
            # Buscar descrição no estoque
            for item_estoque in self.estoque:
                if item_estoque['codigo'] == valores[0]:
                    self.descricao_entry.delete(0, tk.END)
                    self.descricao_entry.insert(0, item_estoque.get('descricao', ''))
                    break
            
            self.valor_entry.delete(0, tk.END)
            self.valor_entry.insert(0, str(valores[2]).replace('R$ ', ''))
            
            self.quantidade_entry.delete(0, tk.END)
            self.quantidade_entry.insert(0, valores[3])
            
    def limpar_campos(self):
        """Limpa todos os campos de entrada"""
        self.codigo_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        
    def atualizar_lista(self):
        """Atualiza a lista de itens na treeview"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Adicionar itens
        for item in self.estoque:
            self.tree.insert('', 'end', values=(
                item['codigo'],
                item['nome'],
                f"R$ {item['valor']:.2f}",
                item['quantidade'],
                f"R$ {item['total']:.2f}"
            ))
            
    def gerar_relatorio(self):
        """Gera relatório de estoque"""
        if not self.estoque:
            return "Estoque vazio.\n\nNenhum item cadastrado no momento."
            
        relatorio = "=" * 50 + "\n"
        relatorio += "RELATÓRIO DE ESTOQUE\n"
        relatorio += "=" * 50 + "\n\n"
        
        total_itens = sum(item['quantidade'] for item in self.estoque)
        valor_total = sum(item['total'] for item in self.estoque)
        media_valor = valor_total / len(self.estoque) if self.estoque else 0
        
        relatorio += f"RESUMO:\n"
        relatorio += f"- Itens diferentes: {len(self.estoque)}\n"
        relatorio += f"- Quantidade total: {total_itens} unidades\n"
        relatorio += f"- Valor total do estoque: R$ {valor_total:.2f}\n"
        relatorio += f"- Valor médio por item: R$ {media_valor:.2f}\n\n"
        
        relatorio += "DETALHAMENTO:\n"
        relatorio += "-" * 70 + "\n"
        
        # Ordenar por código
        estoque_ordenado = sorted(self.estoque, key=lambda x: x['codigo'])
        
        for item in estoque_ordenado:
            relatorio += f"Código: {item['codigo']:<10} | "
            relatorio += f"Nome: {item['nome'][:20]:20} | "
            relatorio += f"Qtd: {item['quantidade']:>4} | "
            relatorio += f"Valor: R$ {item['valor']:>7.2f} | "
            relatorio += f"Total: R$ {item['total']:>8.2f}\n"
            
        relatorio += "-" * 70 + "\n"
        relatorio += f"\nGerado em: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        return relatorio