# clientes_gui.py - Módulo de gestão de clientes

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

class ClientesModule:
    def __init__(self):
        self.clientes_file = "clientes.json"
        self.clientes = []
        self.carregar_clientes()
        
    def carregar_clientes(self):
        """Carrega clientes do arquivo JSON"""
        if os.path.exists(self.clientes_file):
            try:
                with open(self.clientes_file, 'r', encoding='utf-8') as f:
                    self.clientes = json.load(f)
            except:
                self.clientes = []
        else:
            self.clientes = []
            
    def salvar_clientes(self):
        """Salva clientes no arquivo JSON"""
        try:
            with open(self.clientes_file, 'w', encoding='utf-8') as f:
                json.dump(self.clientes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar clientes: {str(e)}")
            
    def validar_cpf(self, cpf):
        """Valida um CPF (validação simplificada)"""
        cpf = re.sub(r'[^0-9]', '', cpf)
        return len(cpf) == 11 and cpf.isdigit()
        
    def formatar_cpf(self, cpf):
        """Formata CPF para exibição"""
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
        
    def create_interface(self, parent):
        """Cria a interface do módulo de clientes"""
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de cadastro (esquerda)
        cadastro_frame = ttk.LabelFrame(main_frame, text="Cadastro de Clientes", padding=10)
        cadastro_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Campos de entrada
        campos = [
            ("CPF:", "cpf_entry"),
            ("Nome Completo:", "nome_entry"),
            ("Telefone:", "telefone_entry"),
            ("Email:", "email_entry"),
            ("Renda Mensal R$:", "renda_entry")
        ]
        
        for i, (label, var_name) in enumerate(campos):
            ttk.Label(cadastro_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(cadastro_frame, width=25)
            entry.grid(row=i, column=1, pady=5, padx=5)
            setattr(self, var_name, entry)
            
        # Botões de ação
        btn_frame = ttk.Frame(cadastro_frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Cadastrar",
                  command=self.cadastrar_cliente,
                  width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remover",
                  command=self.remover_cliente,
                  width=12).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Atualizar",
                  command=self.atualizar_cliente,
                  width=12).pack(side='left', padx=2)
        
        ttk.Button(cadastro_frame, text="Limpar Campos",
                  command=self.limpar_campos,
                  width=25).grid(row=len(campos)+1, column=0, columnspan=2, pady=5)
        
        # Frame da lista (direita)
        list_frame = ttk.LabelFrame(main_frame, text="Clientes Cadastrados", padding=10)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview para mostrar clientes
        columns = ('CPF', 'Nome', 'Telefone', 'Renda')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        col_configs = [
            ('CPF', 120),
            ('Nome', 180),
            ('Telefone', 100),
            ('Renda', 100)
        ]
        
        for col, width in col_configs:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botão para atualizar lista
        ttk.Button(list_frame, text="Atualizar Lista",
                  command=self.atualizar_lista).pack(pady=5)
        
        # Bind para seleção
        self.tree.bind('<<TreeviewSelect>>', self.cliente_selecionado)
        
        # Inicializar lista
        self.atualizar_lista()
        
    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        try:
            cpf = self.cpf_entry.get().strip()
            nome = self.nome_entry.get().strip()
            telefone = self.telefone_entry.get().strip()
            email = self.email_entry.get().strip()
            renda = float(self.renda_entry.get().replace(',', '.')) if self.renda_entry.get() else 0
            
            # Validações
            if not cpf or not nome:
                messagebox.showerror("Erro", "CPF e nome são obrigatórios!")
                return
                
            if not self.validar_cpf(cpf):
                messagebox.showerror("Erro", "CPF inválido! Deve conter 11 dígitos.")
                return
                
            # Verificar se CPF já existe
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            cpf_formatado = self.formatar_cpf(cpf)
            
            for cliente in self.clientes:
                if cliente['cpf_limpo'] == cpf_limpo:
                    messagebox.showerror("Erro", "CPF já cadastrado!")
                    return
            
            # Classificar renda
            if renda < 5000:
                categoria = "Baixa"
            elif renda <= 10000:
                categoria = "Média"
            else:
                categoria = "Alta"
            
            # Adicionar cliente
            novo_cliente = {
                'cpf_formatado': cpf_formatado,
                'cpf_limpo': cpf_limpo,
                'nome': nome,
                'telefone': telefone,
                'email': email,
                'renda': renda,
                'categoria': categoria
            }
            
            self.clientes.append(novo_cliente)
            self.salvar_clientes()
            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valor de renda inválido!")
            
    def remover_cliente(self):
        """Remove cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover!")
            return
            
        item = self.tree.item(selecionado[0])
        cpf_formatado = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Remover cliente {cpf_formatado}?"):
            self.clientes = [c for c in self.clientes if c['cpf_formatado'] != cpf_formatado]
            self.salvar_clientes()
            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
            
    def atualizar_cliente(self):
        """Atualiza cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar!")
            return
            
        try:
            cpf = self.cpf_entry.get().strip()
            nome = self.nome_entry.get().strip()
            telefone = self.telefone_entry.get().strip()
            email = self.email_entry.get().strip()
            renda = float(self.renda_entry.get().replace(',', '.')) if self.renda_entry.get() else 0
            
            # Classificar renda
            if renda < 5000:
                categoria = "Baixa"
            elif renda <= 10000:
                categoria = "Média"
            else:
                categoria = "Alta"
            
            # Atualizar cliente
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            for cliente in self.clientes:
                if cliente['cpf_limpo'] == cpf_limpo:
                    cliente.update({
                        'nome': nome,
                        'telefone': telefone,
                        'email': email,
                        'renda': renda,
                        'categoria': categoria
                    })
                    break
            
            self.salvar_clientes()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valor de renda inválido!")
            
    def cliente_selecionado(self, event):
        """Preenche campos quando cliente é selecionado"""
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado[0])
            valores = item['values']
            
            self.cpf_entry.delete(0, tk.END)
            self.cpf_entry.insert(0, valores[0])
            
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, valores[1])
            
            self.telefone_entry.delete(0, tk.END)
            self.telefone_entry.insert(0, valores[2] if valores[2] != 'Não informado' else "")
            
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, "")
            
            # Buscar dados completos
            for cliente in self.clientes:
                if cliente['cpf_formatado'] == valores[0]:
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(0, cliente.get('email', ''))
                    
                    self.renda_entry.delete(0, tk.END)
                    self.renda_entry.insert(0, f"{cliente['renda']:.2f}")
                    break
                    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.cpf_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.renda_entry.delete(0, tk.END)
        
    def atualizar_lista(self):
        """Atualiza a lista de clientes"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Adicionar clientes
        for cliente in self.clientes:
            telefone = cliente.get('telefone', 'Não informado')
            if not telefone:
                telefone = 'Não informado'
                
            self.tree.insert('', 'end', values=(
                cliente['cpf_formatado'],
                cliente['nome'],
                telefone,
                f"R$ {cliente['renda']:.2f}"
            ))
            
    def gerar_relatorio(self):
        """Gera relatório de clientes"""
        if not self.clientes:
            return "Nenhum cliente cadastrado.\n\nCadastre clientes para gerar relatórios."
            
        relatorio = "=" * 50 + "\n"
        relatorio += "RELATÓRIO DE CLIENTES\n"
        relatorio += "=" * 50 + "\n\n"
        
        total_clientes = len(self.clientes)
        
        # Estatísticas por faixa de renda
        renda_baixa = [c for c in self.clientes if c['categoria'] == 'Baixa']
        renda_media = [c for c in self.clientes if c['categoria'] == 'Média']
        renda_alta = [c for c in self.clientes if c['categoria'] == 'Alta']
        
        renda_total = sum(c['renda'] for c in self.clientes)
        renda_media_cliente = renda_total / total_clientes if total_clientes > 0 else 0
        
        relatorio += f"RESUMO:\n"
        relatorio += f"- Total de clientes: {total_clientes}\n"
        relatorio += f"- Renda total mensal: R$ {renda_total:.2f}\n"
        relatorio += f"- Renda média por cliente: R$ {renda_media_cliente:.2f}\n\n"
        
        relatorio += f"DISTRIBUIÇÃO POR RENDA:\n"
        relatorio += f"- Baixa (< R$ 5.000): {len(renda_baixa)} clientes ({len(renda_baixa)/total_clientes*100:.1f}%)\n"
        relatorio += f"- Média (R$ 5.000-10.000): {len(renda_media)} clientes ({len(renda_media)/total_clientes*100:.1f}%)\n"
        relatorio += f"- Alta (> R$ 10.000): {len(renda_alta)} clientes ({len(renda_alta)/total_clientes*100:.1f}%)\n\n"
        
        relatorio += "LISTA DE CLIENTES:\n"
        relatorio += "-" * 70 + "\n"
        
        # Ordenar por nome
        clientes_ordenados = sorted(self.clientes, key=lambda x: x['nome'])
        
        for cliente in clientes_ordenados:
            relatorio += f"CPF: {cliente['cpf_formatado']} | "
            relatorio += f"Nome: {cliente['nome'][:20]:20} | "
            relatorio += f"Renda: R$ {cliente['renda']:>8.2f} | "
            relatorio += f"Categoria: {cliente['categoria']}\n"
            
        relatorio += "-" * 70 + "\n"
        relatorio += f"\nGerado em: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        return relatorio