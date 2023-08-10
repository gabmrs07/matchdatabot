from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

sep = '_' * 35
token = "5332320571:AAEY0gQYae4u5yLhewmjFS4ic7KaoSY2lGU"


class Bot(object):

    def __init__(self, analyzer):
        """Construtor inicial."""

        self.analyzer = analyzer
        self.updater = Updater(token, use_context=True)
        self.mode = 'normal'
        self.league = ''

        def start(update: Update, context: CallbackContext):
            update.message.reply_text("Bot de escanteios | 23/09/2022 | v0.3")

        def unknown_text(update: Update, context: CallbackContext):
            update.message.reply_text(f'Texto não reconhecido: "{update.message.text}".')

        def unknown(update: Update, context: CallbackContext):
            self.updater.dispatcher.add_handler(CommandHandler('start', start))
            self.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
            self.updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
            self.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

            #msg = update.message.text
            #fav = 'fav_leagues'
            #unfav = 'unfav_leagues'
            #if (self.mode == fav) and (self.league != ''):
             #   sttg = self.analyzer.strategies
              #  if fav not in sttg:
               #     sttg[fav] = []
                #if unfav not in sttg:
                 #   sttg[unfav] = []
 #               if msg == '1':
  #                  if self.league in sttg[unfav]:
   #                     sttg[unfav].remove(self.league)
    #                if self.league not in sttg[fav]:
     #                   sttg[fav].append(self.league)
      #                  reply = f'"{self.league}" foi adicionado às ligas favoritas.'
       #                 self.analyzer.sttg_to_up()
        #            else:
         #               reply = f'"{self.league}" já está em ligas favoritas.'
          #          self.mode = 'normal'
           #         self.league = ''
            #    elif msg == '2':
             #       if self.league in sttg[fav]:
             #           sttg[fav].remove(self.league)
            #        if self.league not in sttg[unfav]:
           #             sttg[unfav].append(self.league)
          #              reply = f'"{self.league}" foi removida das ligas favoritas.'
         #               self.analyzer.sttg_to_up()
        #            else:
       #                 reply = f'"{self.league}" não está em ligas favoritas.'
      #              self.mode = 'normal'
     #               self.league = ''
    #            else:
   #                 reply = f'Qual ação deseja para a competição "{self.league}"?\n(1) Adicionar\n(2) Remover'
  #          elif (self.mode == 'normal') and ("Liga:" in msg):
 #               league = msg.split('\n')[1].split('|')[0].strip('Liga:').strip()
       #         self.mode = 'fav_leagues'
      #          self.league = league
     #           reply = f'Qual ação deseja para a competição "{league}"?\n(1) Adicionar\n(2) Remover'
    #        else:
   #             reply = f'O comando "{msg}" não existe.'
  #          update.message.reply_text(reply)


    def send_message(self, context: CallbackContext, text):
        context.bot.send_message(1885608795, text)

    def run_bot(self):
        self.updater.start_polling()