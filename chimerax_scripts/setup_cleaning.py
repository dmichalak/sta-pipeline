from pathlib import Path

from chimerax.core.commands import run


run(session, 'ui mousemode alt left "move planes"')
run(session, 'ui mousemode right "mark plane"')
run(session, 'ui mousemode alt right "delete picked particle"')