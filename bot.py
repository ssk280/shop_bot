async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ অপারেশন বাতিল করা হয়েছে।")
    return ConversationHandler.END


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    total_profit = (
        shop_state["total_sell_revenue"] - shop_state["total_bought_cost"]
    )

    if text == "📅 তারিখ সেট করুন":
        await update.message.reply_text(
            "দয়া করে এভাবে তারিখ লিখুন: /date [তারিখ]\nউদাহরণ: /date 03 November 2026",
            parse_mode="Markdown",
        )
    elif text == "💰 টোটাল কত সেল হলো":
        await update.message.reply_text(
            f"💰 বর্তমান তারিখের টোটাল সেল: ৳{shop_state['total_sell_revenue']}"
        )
    elif text == "📜 হিস্ট্রি / রিপোর্ট":
        history_text = "📜 শপের সম্পূর্ণ হিস্ট্রি:\n\n"
        if shop_state["history_log"]:
            history_text += (
                "\n".join(shop_state["history_log"]) + "\n\n-------------------\n"
            )

        history_text += (
            f"📌 চলতি তারিখ ({shop_state['current_date']}):\n"
            f"• বিক্রি: {shop_state['total_sold_count']} টি\n"
            f"• খরচ: ৳{shop_state['total_bought_cost']}\n"
            f"• সেল: ৳{shop_state['total_sell_revenue']}\n"
            f"• লাভ: ৳{total_profit}"
        )
        await update.message.reply_text(history_text)
    elif text == "🔄 হিসাব রিসেট":
        shop_state["current_date"] = "তারিখ সেট করা হয়নি"
        shop_state["total_sold_count"] = 0
        shop_state["total_bought_cost"] = 0.0
        shop_state["total_sell_revenue"] = 0.0
        shop_state["history_log"] = []
        await update.message.reply_text(
            "🔄 সব হিসাব এবং হিস্ট্রি সম্পূর্ণ মুছে ফেলা হয়েছে!"
        )


def main():
    TOKEN = "9153410830:AAG_S3UIi5J6akjltqyIuPuzRXZq1z44VPU"

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📦 প্রোডাক্ট সেল হয়েছে$"), start_entry)
        ],
        states={
            GET_COUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_count)
            ],
            GET_BUY_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_buy_price
                )
            ],
            GET_SELL_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_sell_price
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("date", set_date))
    app.add_handler(conv_handler)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)
    )

    print("🤖 Bot with Multi-Day History is running...")
    app.run_polling()


if __name__ == '__main__':
    main()
