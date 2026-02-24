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
            
    def carregar_estoque(self):
        """Carrega o estoque do arquivo JSON para consulta de preços"""
        estoque_file = "estoque.json"
        if os.path.exists(estoque_file):
            try:
                with open(estoque_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_estoque(self, estoque):
        """Salva o estoque atualizado no arquivo JSON"""
        try:
            with open("estoque.json", 'w', encoding='utf-8') as f:
                json.dump(estoque, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar estoque: {str(e)}")
            return False
            
    def atualizar_estoque_apos_venda(self, itens_vendidos):
        """
        Atualiza o estoque após uma venda
        Retorna True se atualizou com sucesso, False caso contrário
        """
        try:
            # Carregar estoque atual
            estoque = self.carregar_estoque()
            
            # Verificar disponibilidade de todos os itens
            for item_venda in itens_vendidos:
                codigo = int(item_venda['codigo'])
                quantidade_vendida = item_venda['quantidade']
                
                # Encontrar item no estoque
                item_encontrado = False
                for item_estoque in estoque:
                    if item_estoque['codigo'] == codigo:
                        item_encontrado = True
                        if item_estoque['quantidade'] < quantidade_vendida:
                            messagebox.showerror("Erro", 
                                f"Estoque insuficiente para {item_estoque['nome']}!\n"
                                f"Disponível: {item_estoque['quantidade']}, Solicitado: {quantidade_vendida}")
                            return False
                        break
                
                if not item_encontrado:
                    messagebox.showerror("Erro", f"Produto código {codigo} não encontrado no estoque!")
                    return False
            
            # Atualizar o estoque
            for item_venda in itens_vendidos:
                codigo = int(item_venda['codigo'])
                quantidade_vendida = item_venda['quantidade']
                
                for item_estoque in estoque:
                    if item_estoque['codigo'] == codigo:
                        # Reduzir a quantidade
                        item_estoque['quantidade'] -= quantidade_vendida
                        # Recalcular o total do item no estoque
                        item_estoque['total'] = item_estoque['quantidade'] * item_estoque['valor']
                        print(f"Estoque atualizado: {item_estoque['nome']} - "
                              f"nova quantidade: {item_estoque['quantidade']}")  # Debug
                        break
            
            # Salvar estoque atualizado
            if self.salvar_estoque(estoque):
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estoque: {str(e)}")
            return False
            
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
        self.codigo_item_entry.bind('<FocusOut>', self.buscar_preco_produto)
        self.codigo_item_entry.bind('<Return>', self.buscar_preco_produto)
        
        ttk.Label(add_frame, text="Qtd:").pack(side='left', padx=2)
        self.qtd_item_entry = ttk.Entry(add_frame, width=5)
        self.qtd_item_entry.pack(side='left', padx=2)
        self.qtd_item_entry.bind('<Return>', lambda e: self.adicionar_item_venda())
        
        # Label para mostrar informações do produto
        self.info_produto_label = ttk.Label(venda_frame, text="", foreground="blue")
        self.info_produto_label.grid(row=4, column=0, columnspan=2, pady=2, sticky='w')
        
        ttk.Button(add_frame, text="+ Adicionar",
                  command=self.adicionar_item_venda,
                  width=12).pack(side='left', padx=5)
        
        # Botão para remover item selecionado
        ttk.Button(venda_frame, text="Remover Item Selecionado",
                  command=self.remover_item_venda,
                  width=20).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Lista de itens da venda atual
        ttk.Label(venda_frame, text="Itens da Venda:", font=('Arial', 10, 'bold')).grid(row=6, column=0, columnspan=2, pady=(10,5), sticky='w')
        
        itens_frame = ttk.Frame(venda_frame)
        itens_frame.grid(row=7, column=0, columnspan=2, pady=5, sticky='nsew')
        
        # Treeview para itens
        columns = ('Código', 'Produto', 'Qtd', 'Valor Unit.', 'Subtotal')
        self.itens_tree = ttk.Treeview(itens_frame, columns=columns, show='headings', height=6)
        
        col_configs = [
            ('Código', 60),
            ('Produto', 120),
            ('Qtd', 50),
            ('Valor Unit.', 80),
            ('Subtotal', 80)
        ]
        
        for col, width in col_configs:
            self.itens_tree.heading(col, text=col)
            self.itens_tree.column(col, width=width)
            
        self.itens_tree.pack()
        
        # Total da venda
        ttk.Label(venda_frame, text="Total da Venda:", 
                 font=('Arial', 11, 'bold')).grid(row=8, column=0, sticky='w', pady=10)
        self.total_venda_label = ttk.Label(venda_frame, text="R$ 0,00", 
                                          font=('Arial', 12, 'bold'), foreground='green')
        self.total_venda_label.grid(row=8, column=1, pady=10, sticky='w')
        
        # Botões da venda
        btn_frame = ttk.Frame(venda_frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=10)
        
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
        columns = ('ID', 'Data', 'CPF', 'Itens', 'Total')
        self.historico_tree = ttk.Treeview(historico_frame, columns=columns, show='headings', height=15)
        
        col_configs = [
            ('ID', 40),
            ('Data', 80),
            ('CPF', 100),
            ('Itens', 80),
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
        
        # Bind para duplo clique no histórico
        self.historico_tree.bind('<Double-1>', self.mostrar_detalhes_venda)
        
        # Botão para atualizar histórico
        ttk.Button(historico_frame, text="Atualizar Histórico",
                  command=self.atualizar_historico).pack(pady=5)
        
        # Inicializar
        self.atualizar_historico()
        
    def buscar_preco_produto(self, event=None):
        """Busca o preço do produto no estoque pelo código"""
        codigo = self.codigo_item_entry.get().strip()
        
        if not codigo:
            self.info_produto_label.config(text="")
            return
            
        try:
            codigo_int = int(codigo)
            estoque = self.carregar_estoque()
            
            # Procurar produto no estoque
            produto_encontrado = None
            for item in estoque:
                if item['codigo'] == codigo_int:
                    produto_encontrado = item
                    break
                    
            if produto_encontrado:
                self.info_produto_label.config(
                    text=f"Produto: {produto_encontrado['nome']} | "
                         f"Preço: R$ {produto_encontrado['valor']:.2f} | "
                         f"Estoque: {produto_encontrado['quantidade']} unidades",
                    foreground="blue"
                )
            else:
                self.info_produto_label.config(
                    text="Produto não encontrado no estoque!",
                    foreground="red"
                )
        except ValueError:
            self.info_produto_label.config(
                text="Código inválido!",
                foreground="red"
            )
        
    def adicionar_item_venda(self):
        """Adiciona item à venda atual, buscando preço do estoque"""
        try:
            codigo = self.codigo_item_entry.get().strip()
            quantidade = int(self.qtd_item_entry.get()) if self.qtd_item_entry.get() else 0
            
            if not codigo or quantidade <= 0:
                messagebox.showerror("Erro", "Código e quantidade são obrigatórios!")
                return
                
            # Buscar produto no estoque
            try:
                codigo_int = int(codigo)
                estoque = self.carregar_estoque()
                
                # Procurar produto no estoque
                produto_encontrado = None
                for item in estoque:
                    if item['codigo'] == codigo_int:
                        produto_encontrado = item
                        break
                        
                if not produto_encontrado:
                    messagebox.showerror("Erro", f"Produto com código {codigo} não encontrado no estoque!")
                    return
                    
                # Verificar quantidade em estoque
                if quantidade > produto_encontrado['quantidade']:
                    messagebox.showerror("Erro", 
                        f"Quantidade insuficiente em estoque!\n"
                        f"Disponível: {produto_encontrado['quantidade']} unidades")
                    return
                    
                valor = produto_encontrado['valor']
                nome_produto = produto_encontrado['nome']
                
            except ValueError:
                messagebox.showerror("Erro", "Código do produto deve ser um número!")
                return
                
            subtotal = quantidade * valor
            
            # Verificar se o item já existe na venda
            for item in self.itens_venda:
                if item['codigo'] == codigo:
                    # Se já existe, perguntar se quer substituir
                    if messagebox.askyesno("Item já existe", 
                        f"O produto {nome_produto} já está na venda com {item['quantidade']} unidades.\n"
                        f"Deseja substituir pela nova quantidade ({quantidade})?"):
                        # Remover item antigo
                        self.itens_venda.remove(item)
                        # Limpar treeview e recriar
                        for row in self.itens_tree.get_children():
                            self.itens_tree.delete(row)
                        for i in self.itens_venda:
                            self.itens_tree.insert('', 'end', values=(
                                i['codigo'],
                                i['nome'][:15] + ('...' if len(i['nome']) > 15 else ''),
                                i['quantidade'],
                                f"R$ {i['valor']:.2f}",
                                f"R$ {i['subtotal']:.2f}"
                            ))
                    else:
                        return
                    break
            
            # Adicionar à lista
            item = {
                'codigo': codigo,
                'nome': nome_produto,
                'quantidade': quantidade,
                'valor': valor,
                'subtotal': subtotal
            }
            self.itens_venda.append(item)
            
            # Adicionar à treeview
            self.itens_tree.insert('', 'end', values=(
                codigo,
                nome_produto[:15] + ('...' if len(nome_produto) > 15 else ''),
                quantidade,
                f"R$ {valor:.2f}",
                f"R$ {subtotal:.2f}"
            ))
            
            # Atualizar total
            self.atualizar_total_venda()
            
            # Limpar campos
            self.codigo_item_entry.delete(0, tk.END)
            self.qtd_item_entry.delete(0, tk.END)
            self.info_produto_label.config(text="")
            
            # Focar no campo de código para próximo item
            self.codigo_item_entry.focus()
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos! Use números.")
            
    def remover_item_venda(self):
        """Remove o item selecionado da venda atual"""
        selecionado = self.itens_tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return
        
        # Obter o item selecionado
        item = self.itens_tree.item(selecionado[0])
        valores = item['values']
        codigo = valores[0]
        
        # Remover da lista
        self.itens_venda = [i for i in self.itens_venda if i['codigo'] != codigo]
        
        # Remover da treeview
        self.itens_tree.delete(selecionado[0])
        
        # Atualizar total
        self.atualizar_total_venda()
        
        messagebox.showinfo("Sucesso", "Item removido da venda!")
            
    def atualizar_total_venda(self):
        """Atualiza o total da venda atual"""
        total = sum(item['subtotal'] for item in self.itens_venda)
        self.total_venda_label.config(text=f"R$ {total:.2f}")
        
    def finalizar_venda(self):
        """Finaliza a venda atual e atualiza o estoque"""
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
            
            # Verificar e atualizar estoque PRIMEIRO
            if not self.atualizar_estoque_apos_venda(self.itens_venda):
                return  # Se falhou em atualizar o estoque, cancela a venda
            
            # Se chegou aqui, o estoque foi atualizado com sucesso
            # Agora podemos registrar a venda
            
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
            
            # Gerar resumo da venda para exibição
            resumo_itens = "\n".join([
                f"  • {item['nome']}: {item['quantidade']} x R$ {item['valor']:.2f} = R$ {item['subtotal']:.2f}"
                for item in self.itens_venda
            ])
            
            messagebox.showinfo("✅ Venda Finalizada", 
                f"Venda #{nova_venda['id']} realizada com sucesso!\n\n"
                f"📅 Data: {data}\n"
                f"👤 Cliente CPF: {cpf}\n"
                f"📦 Itens vendidos:\n{resumo_itens}\n\n"
                f"💰 Total: R$ {total:.2f}\n\n"
                f"📊 Estoque atualizado automaticamente!")
            
            # Limpar venda atual
            self.cancelar_venda()
            self.atualizar_historico()
            
            # Verificar se há itens com estoque baixo
            self.verificar_estoque_baixo()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao finalizar a venda: {str(e)}")
            
    def verificar_estoque_baixo(self):
        """Verifica se há itens com estoque baixo após a venda"""
        estoque = self.carregar_estoque()
        itens_baixo = []
        
        for item in estoque:
            if item['quantidade'] < 5:  # Limite de estoque baixo
                itens_baixo.append(f"{item['nome']} (apenas {item['quantidade']} unidades)")
        
        if itens_baixo:
            messagebox.showwarning("⚠️ Estoque Baixo", 
                "Os seguintes itens estão com estoque baixo:\n\n" + 
                "\n".join(itens_baixo) + 
                "\n\nProvidencie a reposição!")
            
    def cancelar_venda(self):
        """Cancela a venda atual"""
        self.itens_venda = []
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        self.total_venda_label.config(text="R$ 0,00")
        self.cpf_venda_entry.delete(0, tk.END)
        self.info_produto_label.config(text="")
        
    def atualizar_historico(self):
        """Atualiza o histórico de vendas"""
        # Limpar histórico atual
        for item in self.historico_tree.get_children():
            self.historico_tree.delete(item)
            
        # Adicionar vendas (mais recentes primeiro)
        for venda in reversed(self.vendas[-50:]):  # Últimas 50 vendas
            num_itens = len(venda['itens'])
            self.historico_tree.insert('', 'end', values=(
                venda['id'],
                venda['data'],
                venda['cpf'],
                f"{num_itens} itens",
                f"R$ {venda['total']:.2f}"
            ))
            
    def mostrar_detalhes_venda(self, event):
        """Mostra detalhes da venda ao dar duplo clique"""
        selecionado = self.historico_tree.selection()
        if not selecionado:
            return
            
        item = self.historico_tree.item(selecionado[0])
        venda_id = item['values'][0]
        
        # Encontrar a venda
        venda = None
        for v in self.vendas:
            if v['id'] == venda_id:
                venda = v
                break
                
        if venda:
            detalhes = f"📋 DETALHES DA VENDA #{venda_id}\n"
            detalhes += "=" * 40 + "\n\n"
            detalhes += f"📅 Data: {venda['data']}\n"
            detalhes += f"👤 CPF: {venda['cpf']}\n"
            detalhes += f"⏰ Registro: {datetime.fromisoformat(venda['data_registro']).strftime('%d/%m/%Y %H:%M')}\n\n"
            detalhes += "📦 ITENS VENDIDOS:\n"
            
            for item_venda in venda['itens']:
                detalhes += f"  • {item_venda['nome']}\n"
                detalhes += f"    {item_venda['quantidade']} x R$ {item_venda['valor']:.2f} = R$ {item_venda['subtotal']:.2f}\n"
            
            detalhes += f"\n💰 TOTAL: R$ {venda['total']:.2f}"
            
            messagebox.showinfo(f"Venda #{venda_id}", detalhes)
            
    def gerar_relatorio(self):
        """Gera relatório de vendas"""
        if not self.vendas:
            return "Nenhuma venda registrada.\n\nRegistre vendas para gerar relatórios."
            
        relatorio = "=" * 60 + "\n"
        relatorio += "RELATÓRIO DE VENDAS\n"
        relatorio += "=" * 60 + "\n\n"
        
        total_vendas = len(self.vendas)
        valor_total = sum(v['total'] for v in self.vendas)
        media_venda = valor_total / total_vendas if total_vendas > 0 else 0
        
        # Vendas por período
        hoje = datetime.now()
        vendas_hoje = [
            v for v in self.vendas 
            if datetime.fromisoformat(v['data_registro']).date() == hoje.date()
        ]
        
        # Vendas este mês
        vendas_mes = [
            v for v in self.vendas
            if datetime.fromisoformat(v['data_registro']).month == hoje.month
            and datetime.fromisoformat(v['data_registro']).year == hoje.year
        ]
        
        relatorio += "📊 RESUMO:\n"
        relatorio += f"   Total de vendas: {total_vendas}\n"
        relatorio += f"   Valor total vendido: R$ {valor_total:.2f}\n"
        relatorio += f"   Valor médio por venda: R$ {media_venda:.2f}\n"
        relatorio += f"   Vendas hoje: {len(vendas_hoje)}\n"
        relatorio += f"   Vendas este mês: {len(vendas_mes)}\n\n"
        
        relatorio += "📝 ÚLTIMAS VENDAS:\n"
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
            relatorio += "\n🔥 ITENS MAIS VENDIDOS:\n"
            from collections import Counter
            todos_itens = []
            for venda in self.vendas:
                for item in venda['itens']:
                    todos_itens.append(f"{item['codigo']} - {item.get('nome', 'Produto')}")
            
            if todos_itens:
                contador = Counter(todos_itens)
                for item, quantidade in contador.most_common(5):
                    relatorio += f"   • {item}: {quantidade} vendas\n"
        
        relatorio += f"\n📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        return relatorio