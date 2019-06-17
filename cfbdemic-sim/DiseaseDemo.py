import matplotlib.pyplot as plt
import Disease

NFLItis = Disease.disease('NFLItis',1000,1,0,0,0.2,1,1)
time = range(0,100)
healthy = [NFLItis.healthy]
infected = [NFLItis.infected]
contagious = [NFLItis.contagious]
zombified = [NFLItis.zombified]

for n in range(1,100):
    NFLItis.iterate_once()
    healthy = healthy + [NFLItis.healthy]
    infected = infected + [NFLItis.infected]
    contagious = contagious + [NFLItis.contagious]
    zombified = zombified + [NFLItis.zombified]

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(time, healthy, 'b', alpha=0.5, lw=2, label='Healthy')
ax.plot(time, infected, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(time, contagious, 'g', alpha=0.5, lw=2, label='Contagious')
ax.plot(time, zombified, '-y', alpha=0.5, lw=2, label='Zombified')

ax.set_xlabel('Time /days')
ax.set_ylabel('Subpopulation')
ax.set_ylim(0,1200)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)

plt.savefig('diseasedemo.png')
