# Learning to manipulate

This repository contains source code of the following papers:
 * [Learning to combine primitive skills: A step towards versatile robotic manipulation (arxiv);](https://arxiv.org/abs/1908.00722) [Project webpage link](https://www.di.ens.fr/willow/research/rlbc/)
 * [Learning to Augment Synthetic Images for Sim2Real Policy Transfer (IROS'19);](https://arxiv.org/abs/1903.07740) [Project webpage link](http://pascal.inrialpes.fr/data2/sim2real/)

## Learning to combine primitive skills: A step towards versatile robotic manipulation
To reproduce the paper experiments, follow the steps:

### Quickstart

Clone repo:
```bash
git clone https://github.com/rstrudel/rlbc.git rlbc
export RLBC_ROOT=$(pwd)/rlbc
export RLBC_MODELS=$RLBC_ROOT/models
export RLBC_DATA=$RLBC_ROOT/data
mkdir $RLBC_DATA; mkdir $RLBC_MODELS
export PYTHONPATH=$PYTHONPATH:$RLBC_ROOT
```

Install requirements:
```bash
virtualenv -p $(which python3.7) rlbc_env
source rlbc_env/bin/activate

cd $RLBC_ROOT
pip install --upgrade pip
pip install -r requirements.txt
```

Install Manipulation Imitation Environments ([MImE](https://github.com/ikalevatykh/mime-release)):
```bash
git clone https://github.com/ikalevatykh/mime-release.git
cd mime-release
pip install -r requirements.txt
python setup.py develop
```

### BC skills training
1. **Collect a dataset with expert trajectories**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section5/1.pick_collect_demos.json
```
2. **Train a control policy**
```
python3 -m bc.train with $RLBC_ROOT/configs/rlbc/section5/2.pick_train_policy.json
```
3. **Evaluate the policy**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section5/3.pick_evaluate_policy.json
```
4. **Render the policy**

Edit `$RLBC_ROOT/configs/rlbc/section5/4.pick_render_policy.json` and put the best found epoch number there.
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section5/4.pick_render_policy.json
```

### RLBC training
1. **Collect a dataset with expert skills trajectories**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section6/1.bowl_collect_demos.json
```
2. **Train a skills policy**
```
python3 -m bc.train with $RLBC_ROOT/configs/rlbc/section6/2.bowl_train_skills.json
```
3. **Evaluate the skills policy**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section6/3.bowl_evaluate_skills.json
```
4. **Train an RLBC policy**

Edit `$RLBC_ROOT/configs/rlbc/section6/4.bowl_train_rlbc.json` and put the best found epoch number there (`bc.bc_model_epoch` argument). Note that to reproduce the paper results, you may need to train up to 8 policies (by changing `general.seed` argument).
```
python3 -m ppo.train.run with $RLBC_ROOT/configs/rlbc/section6/4.bowl_train_rlbc.json
```
5. **Evaluate the RLBC policy**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/rlbc/section6/5.bowl_evaluate_rlbc.json
```


## Learning to Augment Synthetic Images for Sim2Real Policy Transfer
To train a policy for a real-world UR5 arm, follow the steps:

0. **Collect 200 pairs of robot images and cube positions on a real robot**
 
Save the dataset to `$RLBC_DATA/pick_real`.

1. **Collect 20000 pairs of robot images and cube positions in simulation**
```
python3 -m bc.collect_images with $RLBC_ROOT/configs/autoaug/1.collect_20k_images.json
```

2. **Pretrain a cube position estimation network on a big simulation dataset**
```
python3 -m bc.train with $RLBC_ROOT/configs/autoaug/2.pretrain_checkpoint.json
```

3. **Evaluate epochs of the regression network**
```
python3 -m bc.eval_reg -n regression_checkpoint -d pick_20k
```
Edit `$RLBC_ROOT/configs/autoaug/4.train_mcts.json` and put the best found epoch number there.

4. **Train MCTS using a small simulation dataset**
```
python3 -m sim2real.train with $RLBC_ROOT/configs/autoaug/4.train_mcts.json
```
Edit sim2real.augmentation and add the best augmentation (path) with the name `mcts_learned`.

5. **Collect expert trajectories of picking up a cube**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/autoaug/5.collect_demos.json
```

6. **Train a control policy on augmented expert trajectories**
```
python3 -m bc.train with $RLBC_ROOT/configs/autoaug/6.train_policy.json
```

7. **Evaluate the control policy in simulation**
```
python3 -m bc.collect_demos with $RLBC_ROOT/configs/autoaug/7.evaluate_policy.json
```

8. **Execute the best control policy epoch on a real robot**

Enjoy!


## Citation
If you find this repository helpful, please cite our work:

```
@inproceedings{rlbc2020,
  author    = {Robin Strudel and Alexander Pashevich and Igor Kalevatykh and Ivan Laptev and Josef Sivic and Cordelia Schmid},
  title     = {Learning to combine primitive skills: A step towards versatile robotic manipulation},
  booktitle = {ICRA},
  year      = {2020},
}

@inproceedings{learningsim2real2019,
  author    = {Alexander Pashevich and Robin Strudel and Igor Kalevatykh and Ivan Laptev and Cordelia Schmid},
  title     = {Learning to Augment Synthetic Images for Sim2Real Policy Transfer},
  booktitle = {IROS},
  year      = {2019},
}
```
