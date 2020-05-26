import tensorflow as tf
from TRS_backend.FeatureExtraction.TextFeatureExtraction.fenci_jieba import fenci
import numpy as np
import os
import re
import TRS_backend.FeatureExtraction.TextFeatureExtraction.data_helpers as data_helpers
from tensorflow.contrib import learn
import jieba.posseg

def text_feature_extraction (samples):
    x_raw_list = []
    sentences_list = []
    for sample in samples:
        sentences = re.split(' |。',sample)
        sentences = [item for item in filter(lambda x: x != '', sentences)] #使用过滤器筛掉空串得到了迭代器，再重新构造出列表
        sentences_list.append(sentences)
        x_raw = []
        for sentence in sentences:
            tmp=fenci(sentence)
            x_raw.append(tmp.strip())
        x_raw_list.append(x_raw)

    res = []

    # Eval Parameters
    # tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
    # 填写训练获得模型的存储位置
    curpath = os.path.dirname(os.path.realpath(__file__))
    tf.flags.DEFINE_string("checkpoint_dir", curpath + "\\runs\\TextCNN_model\\checkpoints\\",
                           "Checkpoint directory from training run")
    tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

    # Misc Parameters
    tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
    tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
    FLAGS = tf.flags.FLAGS

    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test_list = []
    for x_raw in x_raw_list:
        x_test = np.array(list(vocab_processor.transform(x_raw)))
        x_test_list.append(x_test)

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
    print("checkpoint_file========", checkpoint_file)

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))

            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            for j in range(len(x_test_list)):
                # Generate batches for one epoch
                batches = data_helpers.batch_iter(list(x_test_list[j]), 64, 1, shuffle=False)
                # 存储模型预测结果
                all_predictions = []
                for x_test_batch in batches:
                    batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                    all_predictions = np.concatenate([all_predictions, batch_predictions])

                problems = []
                procedures = []
                for i in range(len(all_predictions)):
                    short_sentences = sentences_list[j]
                    if all_predictions[i] == 0.0:  # 分类结果为0代表是问题 1代表步骤
                        problems.append(short_sentences[i])
                    else:
                        procedures.append(short_sentences[i])

                # 词法分析获取问题控件
                problem_widget = ''
                last_procedure = ''
                if len(procedures) >= 1:
                    last_procedure = procedures[len(procedures) - 1]
                last_procedure_seged = jieba.posseg.cut(last_procedure.strip())
                first_v = False
                for x in last_procedure_seged:
                    if first_v:
                        if x.flag != 'x' and x.flag != 'm':
                            problem_widget += x.word
                    else:
                        if x.flag == 'v':
                            first_v = True
                            if x.word == '删除':
                                problem_widget = '删除'
                                break
                            if x.word == '输入':
                                problem_widget = '输入框'
                                break
                            if x.word == '搜索':
                                problem_widget = '搜索栏'
                                break
                dict_res = {'procedures_list':procedures,'problem_widget':problem_widget,'problems_list':problems}
                res.append(dict_res)

    return res