#%% plot: compressor, turbine, cavern
idx = pd.IndexSlice
subset = df.loc[idx[["A-TES"], slice(pd.Timestamp('2012-01-01 00:00:00'),
                                     pd.Timestamp('2012-01-04 00:00:00'))], :]

# TODO: Add kwargs dict for common plot properties

fig, axes = plt.subplots(nrows=3, ncols=1)  # figsize=(6,60)
#fig = plt.figure(figsize=(6,8))
dates = subset.index.get_level_values('datetime').unique()
tick_distance = 4 * 24

# compressor
subset['cmp_tr_neg_p_wrk'].plot(ax=axes[0], color=cmap(128), kind="bar",
                                align='center', width=1)
subset['cmp_p_spot'].plot(ax=axes[0], color=cmap(256), kind="bar",
                          align='center', width=1,
                          bottom=subset['cmp_tr_neg_p_wrk'])
axes[0].set_title('Compressor operation', fontsize=30)
axes[0].set_xlabel("")
axes[0].set_xticks(range(0, len(dates), tick_distance), minor=False)
axes[0].set_xticklabels("")
axes[0].set_ylabel("MW", fontsize=30)
axes[0].set_ylim(0, 201)
axes[0].set_yticks(range(0, 201, 50), minor=False)
axes[0].tick_params(axis='x', labelsize=30)
axes[0].tick_params(axis='y', labelsize=30)
axes[0].legend(['Negative control reserve', 'Spot market'], fontsize=30,
               ncol=2)

# turbine
subset['exp_tr_pos_p_wrk'].plot(ax=axes[1], color=cmap(192),
                                kind="bar", align='center', width=1)
subset['exp_p_spot'].plot(ax=axes[1], color=cmap(256), kind="bar",
                          align='center', width=1,
                          bottom=subset['exp_tr_pos_p_wrk'])
axes[1].set_title('Turbine operation', fontsize=30)
axes[1].set_xlabel("")
axes[1].set_xticks(range(0, len(dates), tick_distance), minor=False)
axes[1].set_xticklabels("")
axes[1].set_ylabel("MW", fontsize=30)
axes[1].set_ylim(0, 201)
axes[1].set_yticks(range(0, 201, 50), minor=False)
axes[1].tick_params(axis='x', labelsize=30)
axes[1].tick_params(axis='y', labelsize=30)
axes[1].legend(['Positive control reserve', 'Spot market'], fontsize=30,
               ncol=2)

# cavern
subset['cav_level'].plot(ax=axes[2], color=cmap(96), kind="bar",
                         align='center', width=1)
axes[2].set_title('Cavern filling level', fontsize=30)
axes[2].set_xlabel("")
axes[2].set_xticks(range(0, len(dates), tick_distance), minor=False)
#axes[2].set_xticklabels("")
axes[2].set_ylabel("MWh", fontsize=30)
axes[2].set_ylim(0, 401)
axes[2].set_yticks(range(0, 401, 100), minor=False)
#axes[2].set_yticks(axes[2].get_yticks()[1:])  # remove zero
axes[2].set_xticklabels(
    labels=[item.strftime("%d-%m-%Y")
            for item in dates.tolist()[0::tick_distance]], rotation=0,
    minor=False)  
axes[2].tick_params(axis='x', labelsize=30)
axes[2].tick_params(axis='y', labelsize=30)

# Hide x-ticks at certain positions (first and last label)
xticks = axes[2].xaxis.get_major_ticks()
xticks[0].label1.set_visible(False)
xticks[-1].label1.set_visible(False)

# subplot padding
fig.subplots_adjust(hspace=0.55)
